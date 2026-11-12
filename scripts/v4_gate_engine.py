from __future__ import annotations
import argparse, base64, binascii, hashlib, json, re, shutil, sys, unicodedata
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

ENGINE_ID = "promkes-v4-gate-engine"
ENGINE_VERSION = "0.1.0"
STATUSES = {"NOT_STARTED","IN_PROGRESS","PASS","FAIL","PARTIAL","NOT_RUN","NOT_VERIFIED","NOT_APPLICABLE","BLOCKED","STALE","INVALIDATED"}
NON_PASS = {"NOT_RUN","NOT_VERIFIED","BLOCKED","STALE","INVALIDATED","FAIL","PARTIAL"}
GATES = ["G0_INTAKE_OK","G1_FACT_LOCK","G2_NARRATIVE_LOCK","G3_VISUAL_LOCK","G4_PROMPT_PREFLIGHT","G5_MANIFEST_VALID","G6_CODE_VALID","G7_RELEASE_APPROVED"]
GATE_CONTROLS = {
"G0_INTAKE_OK":{"V4-CTL-012","V4-CTL-013","V4-CTL-015"},
"G1_FACT_LOCK":{"V4-CTL-001","V4-CTL-002","V4-CTL-003","V4-CTL-004"},
"G2_NARRATIVE_LOCK":{"V4-CTL-002","V4-CTL-003"},
"G3_VISUAL_LOCK":{"V4-CTL-021"},
"G4_PROMPT_PREFLIGHT":{"V4-CTL-014"},
"G5_MANIFEST_VALID":{"V4-CTL-005","V4-CTL-006","V4-CTL-007","V4-CTL-008","V4-CTL-009","V4-CTL-019"},
"G6_CODE_VALID":{"V4-CTL-010","V4-CTL-011"},
"G7_RELEASE_APPROVED":{"V4-CTL-016","V4-CTL-017","V4-CTL-018","V4-CTL-020"}}

class EngineError(Exception): pass

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def parse_time(value):
    if not value: return None
    try:
        dt=datetime.fromisoformat(value.replace("Z","+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (TypeError,ValueError): return None

def canonical_json_bytes(value):
    def normalize(obj):
        if isinstance(obj,str): return unicodedata.normalize("NFC",obj.replace("\r\n","\n").replace("\r","\n"))
        if isinstance(obj,list): return [normalize(x) for x in obj]
        if isinstance(obj,dict): return {normalize(str(k)):normalize(v) for k,v in obj.items()}
        return obj
    return json.dumps(normalize(value),sort_keys=True,ensure_ascii=False,separators=(",",":"),allow_nan=False).encode("utf-8")

def sha256_bytes(data): return "sha256:"+hashlib.sha256(data).hexdigest()
def sha256_json(value): return sha256_bytes(canonical_json_bytes(value))

def approval_signature_payload(approval):
    keys=("approval_id","approver_id","role","decision","artifact_hashes","authority_verified","signing_key_id","created_at","expires_at","scope")
    return {key:approval.get(key) for key in keys}

def verify_approval_signature(approval,trusted_keys):
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError as exc: raise EngineError("cryptography is required for Ed25519 approval verification") from exc
    role,key_id=approval.get("role"),approval.get("signing_key_id")
    encoded_key=trusted_keys.get(role,{}).get(key_id)
    if not encoded_key: return False,"signing key is not trusted for this role"
    try:
        public_key=base64.b64decode(encoded_key,validate=True)
        signature=base64.b64decode(approval.get("signature",""),validate=True)
        Ed25519PublicKey.from_public_bytes(public_key).verify(signature,canonical_json_bytes(approval_signature_payload(approval)))
        return True,"Ed25519 signature verified"
    except (ValueError,binascii.Error,TypeError): return False,"malformed Ed25519 key/signature"
    except Exception as exc: return False,f"Ed25519 signature verification failed ({type(exc).__name__})"

def strict_json_load(path):
    def no_dupes(pairs):
        out={}
        for key,value in pairs:
            if key in out: raise EngineError(f"Duplicate JSON key {key!r} in {path}")
            out[key]=value
        return out
    try:
        return json.loads(path.read_text(encoding="utf-8"),object_pairs_hook=no_dupes,parse_constant=lambda x:(_ for _ in ()).throw(EngineError(f"Invalid JSON constant {x}")))
    except OSError as exc: raise EngineError(f"Cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc: raise EngineError(f"Invalid JSON in {path}: {exc}") from exc

def issue(code,message,path="$"): return {"code":code,"path":path,"message":message}

def schema_validate(instance,schema_path):
    try:
        from jsonschema import Draft202012Validator,FormatChecker
    except ImportError as exc: raise EngineError("jsonschema is required; install requirements-dev.txt") from exc
    schema=strict_json_load(schema_path); Draft202012Validator.check_schema(schema)
    validator=Draft202012Validator(schema,format_checker=FormatChecker()); errors=[]
    for err in sorted(validator.iter_errors(instance),key=lambda e:(list(map(str,e.path)),e.message)):
        path="$"+"".join((f"[{p}]" if isinstance(p,int) else f".{p}" for p in err.path))
        errors.append(issue("SCHEMA_INVALID",err.message,path))
    return errors

def index_records(items,key):
    result={}; errors=[]
    for i,item in enumerate(items):
        identifier=item.get(key)
        if not isinstance(identifier,str) or not identifier.strip(): errors.append(issue("ID_MISSING",f"{key} must be a non-empty string",f"$[{i}].{key}"))
        elif identifier in result: errors.append(issue("ID_DUPLICATE",f"Duplicate {key}: {identifier}",f"$[{i}].{key}"))
        else: result[identifier]=item
    return result,errors

def safe_relative_path(raw):
    if not isinstance(raw,str) or not raw or "\\" in raw or "\x00" in raw: return False
    p=PurePosixPath(raw)
    return not p.is_absolute() and all(part not in {"",".",".."} for part in raw.split("/"))

def resolve_project_path(project_file,raw):
    if not safe_relative_path(raw): return None
    root=project_file.resolve().parent; candidate=(root/Path(*PurePosixPath(raw).parts)).resolve()
    try: candidate.relative_to(root)
    except ValueError: return None
    return candidate

def dependency_graph(project):
    nodes=set()
    for bucket,key in (("artifacts","artifact_id"),("claims","claim_id"),("scenes","scene_id"),("sources","source_id")):
        nodes.update(row[key] for row in project.get(bucket,[]) if isinstance(row.get(key),str))
    graph=defaultdict(set); errors=[]
    for i,edge in enumerate(project.get("dependencies",[])):
        parent,child=edge.get("from_id"),edge.get("to_id")
        if parent not in nodes or child not in nodes: errors.append(issue("DEPENDENCY_UNKNOWN",f"Unknown dependency endpoint {parent!r} -> {child!r}",f"$.dependencies[{i}]")); continue
        graph[parent].add(child)
    indegree={node:0 for node in nodes}
    for parent in graph:
        for child in graph[parent]: indegree[child]+=1
    queue=deque(sorted(n for n,d in indegree.items() if d==0)); seen=0
    while queue:
        node=queue.popleft(); seen+=1
        for child in sorted(graph.get(node,set())):
            indegree[child]-=1
            if indegree[child]==0: queue.append(child)
    if seen!=len(indegree): errors.append(issue("DEPENDENCY_CYCLE","Dependency graph contains a directed cycle"))
    return graph,errors

def semantic_validate(project,project_file,now=None):
    errors=[]; now=now or datetime.now(timezone.utc)
    source_map,e=index_records(project.get("sources",[]),"source_id"); errors.extend(e)
    claim_map,e=index_records(project.get("claims",[]),"claim_id"); errors.extend(e)
    scene_map,e=index_records(project.get("scenes",[]),"scene_id"); errors.extend(e)
    artifact_map,e=index_records(project.get("artifacts",[]),"artifact_id"); errors.extend(e)
    caps,e=index_records(project.get("capabilities",[]),"capability_id"); errors.extend(e)
    for i,source in enumerate(project.get("sources",[])):
        if source.get("verification_status")=="VERIFIED":
            if not source.get("source_uri") or not source.get("support_location"): errors.append(issue("SOURCE_PROVENANCE_INCOMPLETE","Verified source requires source_uri and support_location",f"$.sources[{i}]"))
            if not re.fullmatch("sha256:[a-fA-F0-9]{64}",str(source.get("content_hash",""))): errors.append(issue("SOURCE_HASH_INVALID","Verified source requires a SHA-256 content_hash",f"$.sources[{i}].content_hash"))
            if not parse_time(source.get("accessed_at")): errors.append(issue("SOURCE_ACCESS_TIME_INVALID","Verified source requires an ISO-8601 accessed_at",f"$.sources[{i}].accessed_at"))
    blocked={"UNVERIFIED","CONTRADICTED","UNKNOWN","STALE"}
    for i,claim in enumerate(project.get("claims",[])):
        for sid in claim.get("source_ids",[]):
            if sid not in source_map: errors.append(issue("CLAIM_SOURCE_MISSING",f"Claim references unknown source {sid}",f"$.claims[{i}].source_ids"))
        status=claim.get("status")
        if status in blocked and claim.get("allowed_wording"): errors.append(issue("CLAIM_WORDING_FAIL_CLOSED",f"{status} claim cannot contain allowed_wording",f"$.claims[{i}].allowed_wording"))
        material=claim.get("claim_type") in {"PREVENTION","TREATMENT","RISK","STATISTIC","CAUSAL"}
        if material and status=="VERIFIED":
            if not claim.get("source_ids"): errors.append(issue("MATERIAL_CLAIM_UNSOURCED","Material VERIFIED claim requires at least one source",f"$.claims[{i}].source_ids"))
            if not claim.get("reviewed_by_human") or claim.get("reviewer_role")!="CLINICIAN" or not claim.get("reviewer_id") or not parse_time(claim.get("reviewed_at")):
                errors.append(issue("CLINICAL_REVIEW_MISSING","Material VERIFIED health claim requires named clinician review and timestamp",f"$.claims[{i}]"))
        if status=="VERIFIED" and any(sid in source_map and source_map[sid].get("verification_status")!="VERIFIED" for sid in claim.get("source_ids",[])):
            errors.append(issue("CLAIM_SOURCE_NOT_VERIFIED","VERIFIED claim references a source not marked VERIFIED",f"$.claims[{i}].source_ids"))
        if status in {"PARTIALLY_SUPPORTED","MIXED"} and material:
            if not claim.get("reviewed_by_human") or claim.get("reviewer_role")!="CLINICIAN" or not claim.get("allowed_wording"):
                errors.append(issue("CONSTRAINED_CLAIM_REVIEW_MISSING","PARTIALLY_SUPPORTED/MIXED material claim requires clinician-approved constrained wording",f"$.claims[{i}]"))
    ordered=sorted(project.get("scenes",[]),key=lambda s:(s.get("order",-1),s.get("scene_id",""))); previous_end=None; fps_values=set()
    for i,scene in enumerate(ordered):
        start,end,fps=scene.get("start_frame"),scene.get("end_frame"),scene.get("fps")
        if not isinstance(start,int) or not isinstance(end,int) or start<0 or end<=start: errors.append(issue("SCENE_FRAME_RANGE_INVALID","Scene frame interval must be non-negative and have end_frame > start_frame",f"$.scenes[{i}]"))
        if not isinstance(fps,(int,float)) or isinstance(fps,bool) or fps<=0: errors.append(issue("SCENE_FPS_INVALID","fps must be a positive number",f"$.scenes[{i}].fps"))
        else: fps_values.add(fps)
        if previous_end is not None and isinstance(start,int) and start!=previous_end: errors.append(issue("SCENE_TIMELINE_GAP_OR_OVERLAP",f"Expected start_frame {previous_end}, received {start}",f"$.scenes[{i}].start_frame"))
        if isinstance(end,int): previous_end=end
        for cid in scene.get("claim_refs",[]):
            if cid not in claim_map: errors.append(issue("SCENE_CLAIM_UNKNOWN",f"Unknown claim reference {cid}",f"$.scenes[{i}].claim_refs"))
    if len(fps_values)>1: errors.append(issue("SCENE_FPS_MISMATCH","All scenes in one timeline must use the same fps unless explicitly segmented"))
    for i,asset in enumerate(project.get("assets",[])):
        raw=asset.get("path")
        if not safe_relative_path(raw): errors.append(issue("ASSET_PATH_UNSAFE",f"Unsafe asset path: {raw!r}",f"$.assets[{i}].path")); continue
        target=resolve_project_path(project_file,raw)
        if target is None: errors.append(issue("ASSET_PATH_ESCAPE",f"Asset path escapes project root: {raw}",f"$.assets[{i}].path")); continue
        cursor=project_file.resolve().parent
        for part in PurePosixPath(raw).parts:
            cursor=cursor/part
            if cursor.is_symlink(): errors.append(issue("ASSET_SYMLINK_FORBIDDEN",f"Symlink asset path is forbidden: {raw}",f"$.assets[{i}].path")); break
        if asset.get("required",True) and not target.is_file(): errors.append(issue("ASSET_MISSING",f"Required asset does not exist: {raw}",f"$.assets[{i}].path"))
        if target.is_file() and asset.get("content_hash"):
            actual=sha256_bytes(target.read_bytes())
            if actual.lower()!=str(asset["content_hash"]).lower(): errors.append(issue("ASSET_HASH_MISMATCH",f"Asset hash mismatch: {raw}",f"$.assets[{i}].content_hash"))
    for i,artifact in enumerate(project.get("artifacts",[])):
        for sid in artifact.get("source_refs",[]):
            if sid not in source_map: errors.append(issue("ARTIFACT_SOURCE_UNKNOWN",f"Unknown source ref {sid}",f"$.artifacts[{i}].source_refs"))
        known=set(source_map)|set(claim_map)|set(scene_map)|set(artifact_map)|set(caps)
        for dep in artifact.get("dependency_refs",[]):
            if dep not in known: errors.append(issue("ARTIFACT_DEPENDENCY_UNKNOWN",f"Unknown dependency ref {dep}",f"$.artifacts[{i}].dependency_refs"))
        if artifact.get("status")=="PASS" and artifact.get("validation_result") not in {"PASS","NOT_APPLICABLE"}:
            errors.append(issue("ARTIFACT_STATUS_ESCALATION","Artifact status PASS conflicts with validation_result",f"$.artifacts[{i}].status"))
        if artifact.get("content_path"):
            target=resolve_project_path(project_file,artifact["content_path"])
            if target is None or not target.is_file(): errors.append(issue("ARTIFACT_CONTENT_MISSING","Artifact content_path must resolve to an existing file inside project root",f"$.artifacts[{i}].content_path"))
            elif sha256_bytes(target.read_bytes()).lower()!=str(artifact.get("content_hash","")).lower():
                errors.append(issue("ARTIFACT_HASH_MISMATCH","Artifact content hash does not match file bytes",f"$.artifacts[{i}].content_hash"))
    graph,graph_errors=dependency_graph(project); errors.extend(graph_errors)
    for i,cap in enumerate(project.get("capabilities",[])):
        if cap.get("status")=="VERIFIED":
            if not cap.get("provider") or not cap.get("operation") or not cap.get("exact_version"): errors.append(issue("CAPABILITY_VERSION_INCOMPLETE","VERIFIED capability requires provider, operation and exact_version",f"$.capabilities[{i}]"))
            if cap.get("permission_granted") is not True or not cap.get("evidence_ref"): errors.append(issue("CAPABILITY_EVIDENCE_MISSING","VERIFIED capability requires permission_granted=true and evidence_ref",f"$.capabilities[{i}]"))
            checked,expires=parse_time(cap.get("checked_at")),parse_time(cap.get("expires_at"))
            if not checked or not expires or expires<=now: errors.append(issue("CAPABILITY_EXPIRED_OR_UNDATED","VERIFIED capability requires checked_at and future expires_at",f"$.capabilities[{i}]"))
    trusted=project.get("authorized_approvers",{}); trusted_keys=project.get("trusted_signing_keys",{})
    known_hashes={a.get("content_hash") for a in project.get("artifacts",[])}
    known_hashes.update(sha256_json(c) for c in project.get("claims",[]))
    rights_hash=project.get("policy",{}).get("rights_evidence_hash")
    if rights_hash: known_hashes.add(rights_hash)
    visual_hash=project.get("visual",{}).get("canonical_reference_hash")
    if visual_hash: known_hashes.add(visual_hash)
    qa_hash=project.get("artifact_qa",{}).get("artifact_hash")
    if qa_hash: known_hashes.add(qa_hash)
    for i,approval in enumerate(project.get("approvals",[])):
        role,person=approval.get("role"),approval.get("approver_id")
        if approval.get("decision")=="APPROVED":
            if person not in trusted.get(role,[]): errors.append(issue("APPROVER_NOT_AUTHORIZED",f"Approver {person!r} is not in authorized_approvers[{role!r}]",f"$.approvals[{i}]"))
            if approval.get("authority_verified") is not True: errors.append(issue("APPROVER_AUTHORITY_UNVERIFIED","Approval authority has not been independently verified",f"$.approvals[{i}].authority_verified"))
            sig_ok,sig_message=verify_approval_signature(approval,trusted_keys)
            if not sig_ok: errors.append(issue("APPROVAL_SIGNATURE_UNVERIFIED",sig_message,f"$.approvals[{i}].signature"))
            if not approval.get("artifact_hashes") or not set(approval.get("artifact_hashes",[])).issubset(known_hashes):
                errors.append(issue("APPROVAL_NOT_HASH_BOUND","Approval hashes must bind to known artifact/claim/QA hashes",f"$.approvals[{i}].artifact_hashes"))
            expires=parse_time(approval.get("expires_at"))
            if expires and expires<=now: errors.append(issue("APPROVAL_EXPIRED","Approval has expired",f"$.approvals[{i}].expires_at"))
    policy=project.get("policy",{})
    if policy.get("rights_status","UNKNOWN") not in {"CLEARED","NOT_APPLICABLE"}: errors.append(issue("RIGHTS_NOT_CLEARED","Rights status must be CLEARED or justified NOT_APPLICABLE","$.policy.rights_status"))
    if policy.get("privacy_classification","UNKNOWN")=="UNKNOWN": errors.append(issue("PRIVACY_CLASSIFICATION_UNKNOWN","Privacy classification must be explicit","$.policy.privacy_classification"))
    security=project.get("security_review",{})
    if security.get("status")!="PASS" or security.get("untrusted_content_isolated") is not True:
        errors.append(issue("SECURITY_REVIEW_NOT_PASSED","Security review and untrusted-content isolation must pass","$.security_review"))
    budget=project.get("budget",{})
    if budget:
        for actual,ceiling in (("estimated_cost","budget_limit"),("actual_cost","budget_limit"),("retry_count","max_retries"),("asset_bytes","max_asset_bytes")):
            if actual in budget and ceiling in budget and budget[actual]>budget[ceiling]: errors.append(issue("RESOURCE_CEILING_EXCEEDED",f"{actual} exceeds {ceiling}",f"$.budget.{actual}"))
    return errors

def project_subject_hash(project):
    subject=dict(project); subject.pop("control_results",None); return sha256_json(subject)

def valid_control_evidence(record,project=None):
    required=("control_id","test_id","oracle","observed","executed_at","environment","engine_version","subject_hash","evidence_hash")
    if any(not record.get(k) for k in required): return False
    if not parse_time(record.get("executed_at")) or record.get("engine_version")!=ENGINE_VERSION: return False
    if not re.fullmatch("sha256:[a-fA-F0-9]{64}",str(record.get("subject_hash",""))): return False
    if project is not None and record.get("subject_hash")!=project_subject_hash(project): return False
    expected=sha256_json({k:v for k,v in record.items() if k!="evidence_hash"})
    return expected.lower()==str(record.get("evidence_hash","")).lower()

def local_gate_check(project,gate,project_file,now=None):
    reasons=[]; now=now or datetime.now(timezone.utc)
    if gate not in GATES: return "FAIL",[f"Unknown gate: {gate}"]
    results={r.get("control_id"):r for r in project.get("control_results",[])}
    for control_id in sorted(GATE_CONTROLS[gate]):
        rec=results.get(control_id)
        if not rec or rec.get("status")!="PASS" or not valid_control_evidence(rec,project):
            reasons.append(f"Required executable control {control_id} lacks valid PASS evidence")
    if gate=="G0_INTAKE_OK":
        if not project.get("sources"): reasons.append("Source inventory is empty")
        if project.get("policy",{}).get("rights_status") not in {"CLEARED","NOT_APPLICABLE"}: reasons.append("Rights are not cleared")
        if project.get("policy",{}).get("privacy_classification") in {None,"UNKNOWN"}: reasons.append("Privacy classification is unknown")
        if project.get("security_review",{}).get("status")!="PASS": reasons.append("Security review is not PASS")
        if project.get("security_review",{}).get("untrusted_content_isolated") is not True: reasons.append("Untrusted content is not explicitly isolated")
        rights_hash=project.get("policy",{}).get("rights_evidence_hash")
        if project.get("policy",{}).get("rights_status")=="CLEARED" and not any(a.get("role")=="RIGHTS_APPROVER" and a.get("decision")=="APPROVED" and rights_hash in a.get("artifact_hashes",[]) and verify_approval_signature(a,project.get("trusted_signing_keys",{}))[0] for a in project.get("approvals",[])):
            reasons.append("Rights clearance lacks a signed, hash-bound RIGHTS_APPROVER record")
    elif gate=="G1_FACT_LOCK":
        for claim in project.get("claims",[]):
            if claim.get("status") not in {"VERIFIED","PARTIALLY_SUPPORTED","MIXED"}: reasons.append(f"Claim {claim.get('claim_id')} is {claim.get('status')}, not fact-lock eligible")
            if claim.get("claim_type") in {"PREVENTION","TREATMENT","RISK","STATISTIC","CAUSAL"}:
                signed=any(a.get("role")=="CLINICIAN" and a.get("decision")=="APPROVED" and sha256_json(claim) in a.get("artifact_hashes",[]) and verify_approval_signature(a,project.get("trusted_signing_keys",{}))[0] for a in project.get("approvals",[]))
                if claim.get("reviewer_role")!="CLINICIAN" or not signed: reasons.append(f"Material claim {claim.get('claim_id')} lacks signed clinician review")
    elif gate=="G2_NARRATIVE_LOCK":
        narrative=project.get("narrative",{})
        if narrative.get("review_status")!="PASS": reasons.append("Narrative review is not PASS")
        for cid in narrative.get("claim_refs",[]):
            if not any(c.get("claim_id")==cid and c.get("status") in {"VERIFIED","PARTIALLY_SUPPORTED","MIXED"} for c in project.get("claims",[])): reasons.append(f"Narrative references claim not eligible for use: {cid}")
    elif gate=="G3_VISUAL_LOCK":
        visual=project.get("visual",{}); vh=visual.get("canonical_reference_hash")
        signed=any(a.get("role")=="BRAND_OWNER" and a.get("decision")=="APPROVED" and vh in a.get("artifact_hashes",[]) and verify_approval_signature(a,project.get("trusted_signing_keys",{}))[0] for a in project.get("approvals",[]))
        if visual.get("review_status")!="PASS" or not re.fullmatch("sha256:[a-fA-F0-9]{64}",str(vh or "")) or not visual.get("reviewed_by") or not parse_time(visual.get("reviewed_at")) or not signed:
            reasons.append("Visual continuity requires reviewer/timestamp/canonical hash and signed BRAND_OWNER approval")
    elif gate=="G4_PROMPT_PREFLIGHT":
        pre=project.get("prompt_preflight",{})
        if pre.get("status")!="PASS" or pre.get("untrusted_source_labels_present") is not True: reasons.append("Prompt preflight or untrusted source labelling has not passed")
        if pre.get("source_instructions_executed") is not False: reasons.append("Source-embedded instructions are not attested as non-executed")
    elif gate=="G5_MANIFEST_VALID":
        if not project.get("scenes"): reasons.append("Scene manifest is empty")
        if semantic_validate(project,project_file,now): reasons.append("Project has semantic validation errors")
        if any(a.get("validation_result")!="PASS" for a in project.get("artifacts",[])): reasons.append("One or more artifact validation results are not PASS")
    elif gate=="G6_CODE_VALID":
        target=project.get("renderer_target",{})
        if target.get("executable_code_required"):
            found=[c for c in project.get("capabilities",[]) if c.get("operation")=="render" and c.get("provider")==target.get("provider") and c.get("exact_version")==target.get("exact_version") and c.get("status")=="VERIFIED"]
            if not found: reasons.append("Exact renderer capability is not VERIFIED")
        if project.get("code_review",{}).get("status")!="PASS": reasons.append("Code review is not PASS")
        if project.get("code_review",{}).get("sandbox_evidence_ref") is None: reasons.append("Sandbox evidence is missing")
    elif gate=="G7_RELEASE_APPROVED":
        if project.get("project_mode")!="PRODUCTION": reasons.append("TEST_FIXTURE or unspecified project_mode cannot enter the production release gate")
        qa_hash=project.get("artifact_qa",{}).get("artifact_hash")
        verified={a.get("content_hash") for a in project.get("artifacts",[]) if a.get("status")=="PASS" and a.get("validation_result")=="PASS"}
        if project.get("artifact_qa",{}).get("status")!="PASS" or not qa_hash or qa_hash not in verified: reasons.append("Artifact QA is not PASS or does not reference a content-hash-verified artifact")
        if project.get("release",{}).get("status")!="APPROVED": reasons.append("Release approval is not APPROVED")
        signed=any(a.get("decision")=="APPROVED" and a.get("role")=="RELEASE_APPROVER" and qa_hash in a.get("artifact_hashes",[]) and verify_approval_signature(a,project.get("trusted_signing_keys",{}))[0] for a in project.get("approvals",[]))
        if not signed: reasons.append("Cryptographically verified, hash-bound RELEASE_APPROVER record is missing")
    return ("PASS",[]) if not reasons else ("BLOCKED",reasons)

def evaluate_gates(project,project_file,target=None,now=None):
    target=target or GATES[-1]
    if target not in GATES: raise EngineError(f"Unknown gate {target}")
    results=[]; predecessor_failed=False
    for gate in GATES[:GATES.index(target)+1]:
        if predecessor_failed: status,reasons="BLOCKED",["A predecessor gate is not PASS; downstream transition is prohibited"]
        else: status,reasons=local_gate_check(project,gate,project_file,now)
        results.append({"gate":gate,"status":status,"reasons":reasons})
        if status!="PASS": predecessor_failed=True
    return {"target_gate":target,"overall":"PASS" if results[-1]["status"]=="PASS" else "BLOCKED","gates":results}

def compute_invalidations(project,changed_id):
    graph,errors=dependency_graph(project)
    if errors: raise EngineError("Cannot compute invalidation with invalid dependency graph: "+"; ".join(x["message"] for x in errors))
    invalidated=set(); queue=deque(graph.get(changed_id,set()))
    while queue:
        node=queue.popleft()
        if node==changed_id or node in invalidated: continue
        invalidated.add(node); queue.extend(graph.get(node,set()))
    return sorted(invalidated)

CONTROL_REGISTRY=[
("V4-CTL-001","claim_source_integrity","Every claim source reference resolves"),
("V4-CTL-002","claim_fail_closed","Unverified/contradicted/unknown/stale claims cannot authorize wording"),
("V4-CTL-003","clinical_review","Material health claims require clinician review"),
("V4-CTL-004","source_provenance","Verified sources carry provenance and content hash"),
("V4-CTL-005","scene_timing","Scene ranges are valid, ordered, contiguous and consistent"),
("V4-CTL-006","scene_identity","Scene identifiers are unique"),
("V4-CTL-007","dependency_integrity","Dependencies resolve and form a DAG"),
("V4-CTL-008","asset_path_safety","Asset paths are confined to project root"),
("V4-CTL-009","artifact_hash_integrity","Artifact files match their declared SHA-256"),
("V4-CTL-010","capability_evidence","Verified capabilities are specific, evidenced and current"),
("V4-CTL-011","renderer_fail_closed","Executable code cannot route to unverified target runtime"),
("V4-CTL-012","rights_clearance","Rights are cleared or explicitly not applicable"),
("V4-CTL-013","privacy_classification","Privacy classification cannot remain unknown"),
("V4-CTL-014","prompt_firewall","Untrusted source content is isolated and not executed as instructions"),
("V4-CTL-015","resource_ceiling","Cost, retry and asset ceilings are enforced"),
("V4-CTL-016","approval_hash_binding","Human approvals are authorized and bound to artifact hashes"),
("V4-CTL-017","gate_fail_closed","Gate transition cannot pass without predecessor evidence"),
("V4-CTL-018","invalidation_propagation","Upstream changes invalidate transitive dependents"),
("V4-CTL-019","artifact_status_integrity","Artifact status cannot be elevated beyond validation result"),
("V4-CTL-020","control_evidence_integrity","PASS control result includes execution/evidence metadata"),
("V4-CTL-021","visual_reference_lock","Visual continuity has an approved canonical reference hash")]

def control_check(project,project_file,adapter,now=None):
    now=now or datetime.now(timezone.utc); semantic=semantic_validate(project,project_file,now)
    if adapter=="claim_source_integrity":
        sources={s.get("source_id") for s in project.get("sources",[])}
        missing=[(c.get("claim_id"),sid) for c in project.get("claims",[]) for sid in c.get("source_ids",[]) if sid not in sources]
        return not missing,f"missing claim-source refs={missing}"
    if adapter=="claim_fail_closed":
        bad=[c.get("claim_id") for c in project.get("claims",[]) if c.get("status") in {"UNVERIFIED","CONTRADICTED","UNKNOWN","STALE"} and c.get("allowed_wording")]
        return not bad,f"claims with unauthorized wording={bad}"
    if adapter=="clinical_review":
        bad=[]
        for c in project.get("claims",[]):
            if c.get("claim_type") in {"PREVENTION","TREATMENT","RISK","STATISTIC","CAUSAL"} and c.get("status") in {"VERIFIED","PARTIALLY_SUPPORTED","MIXED"}:
                ch=sha256_json(c)
                signed=any(a.get("role")=="CLINICIAN" and a.get("decision")=="APPROVED" and ch in a.get("artifact_hashes",[]) and verify_approval_signature(a,project.get("trusted_signing_keys",{}))[0] for a in project.get("approvals",[]))
                if c.get("reviewer_role")!="CLINICIAN" or not signed: bad.append(c.get("claim_id"))
        return not bad,f"material claims without signed clinician review={bad}"
    if adapter=="source_provenance":
        referenced={sid for c in project.get("claims",[]) if c.get("status")=="VERIFIED" for sid in c.get("source_ids",[])}
        sm={s.get("source_id"):s for s in project.get("sources",[])}
        bad=[sid for sid in referenced if sid not in sm or sm[sid].get("verification_status")!="VERIFIED"]
        bad += [s.get("source_id") for s in project.get("sources",[]) if s.get("verification_status")=="VERIFIED" and (not re.fullmatch("sha256:[a-fA-F0-9]{64}",str(s.get("content_hash",""))) or not s.get("source_uri") or not s.get("support_location") or not parse_time(s.get("accessed_at")))]
        return not bad,f"verified source provenance defects={sorted(set(bad))}"
    if adapter=="scene_timing":
        se=[x for x in semantic if x["code"].startswith("SCENE_")]; return bool(project.get("scenes")) and not se,f"scene_count={len(project.get('scenes',[]))}; scene_errors={se}"
    if adapter=="scene_identity":
        _,errs=index_records(project.get("scenes",[]),"scene_id"); return not errs,f"scene identity errors={errs}"
    if adapter=="dependency_integrity":
        _,errs=dependency_graph(project); return not errs,f"dependency errors={errs}"
    if adapter=="asset_path_safety":
        bad=[a.get("path") for a in project.get("assets",[]) if not safe_relative_path(a.get("path")) or resolve_project_path(project_file,a.get("path","")) is None]
        return not bad,f"unsafe asset paths={bad}"
    if adapter=="artifact_hash_integrity":
        bad=[a.get("artifact_id") for a in project.get("artifacts",[]) if not a.get("content_path") or any(x["code"] in {"ARTIFACT_HASH_MISMATCH","ARTIFACT_CONTENT_MISSING"} for x in semantic)]
        return bool(project.get("artifacts")) and not bad,f"artifact hash/content defects={bad}"
    if adapter=="capability_evidence":
        bad=[c.get("capability_id") for c in project.get("capabilities",[]) if c.get("status")=="VERIFIED" and any(x["code"] in {"CAPABILITY_VERSION_INCOMPLETE","CAPABILITY_EVIDENCE_MISSING","CAPABILITY_EXPIRED_OR_UNDATED"} for x in semantic)]
        return not bad,f"invalid verified capabilities={bad}"
    if adapter=="renderer_fail_closed":
        t=project.get("renderer_target",{})
        if not t.get("executable_code_required"): return True,"no target-specific executable code requested"
        ok=any(c.get("provider")==t.get("provider") and c.get("operation")=="render" and c.get("exact_version")==t.get("exact_version") and c.get("status")=="VERIFIED" for c in project.get("capabilities",[]))
        return ok,"exact target capability verified" if ok else "target-specific executable code blocked"
    if adapter=="rights_clearance":
        ok=project.get("policy",{}).get("rights_status") in {"CLEARED","NOT_APPLICABLE"}; return ok,f"rights_status={project.get('policy',{}).get('rights_status','UNKNOWN')}"
    if adapter=="privacy_classification":
        ok=project.get("policy",{}).get("privacy_classification") not in {None,"UNKNOWN"}; return ok,"privacy classification explicit" if ok else "privacy classification UNKNOWN"
    if adapter=="prompt_firewall":
        p=project.get("prompt_preflight",{}); ok=p.get("status")=="PASS" and p.get("untrusted_source_labels_present") is True and p.get("source_instructions_executed") is False
        return ok,"prompt boundary attested" if ok else "untrusted-source firewall not proven"
    if adapter=="resource_ceiling":
        b=project.get("budget",{}); pairs=(("estimated_cost","budget_limit"),("actual_cost","budget_limit"),("retry_count","max_retries"),("asset_bytes","max_asset_bytes"))
        bad=[f"{a}>{c}" for a,c in pairs if a in b and c in b and b[a]>b[c]]
        return not bad,f"resource ceiling violations={bad}"
    if adapter=="approval_hash_binding":
        trusted=project.get("authorized_approvers",{}); keys=project.get("trusted_signing_keys",{})
        hashes={a.get("content_hash") for a in project.get("artifacts",[])}; hashes.add(project.get("artifact_qa",{}).get("artifact_hash"))
        hashes.update(sha256_json(c) for c in project.get("claims",[]))
        rh=project.get("policy",{}).get("rights_evidence_hash")
        if rh: hashes.add(rh)
        vh=project.get("visual",{}).get("canonical_reference_hash")
        if vh: hashes.add(vh)
        bad=[a.get("approval_id") for a in project.get("approvals",[]) if a.get("decision")=="APPROVED" and (a.get("approver_id") not in trusted.get(a.get("role"),[]) or a.get("authority_verified") is not True or not verify_approval_signature(a,keys)[0] or not a.get("artifact_hashes") or not set(a.get("artifact_hashes",[])).issubset(hashes))]
        return not bad and bool(project.get("approvals")),f"invalid approvals={bad}"
    if adapter=="gate_fail_closed":
        probe=dict(project); probe["control_results"]=[]
        report=evaluate_gates(probe,project_file,"G1_FACT_LOCK",now)
        blocked=report["overall"]=="BLOCKED" and all(g["status"]!="PASS" for g in report["gates"])
        return blocked,"empty evidence set blocks transition as required" if blocked else "gate transition incorrectly passed without evidence"
    if adapter=="invalidation_propagation":
        changed=project.get("invalidation_test",{}).get("changed_id"); expected=set(project.get("invalidation_test",{}).get("expected_invalidated",[]))
        if not changed: return False,"invalidation_test.changed_id fixture is required to exercise this control"
        actual=set(compute_invalidations(project,changed)); return actual==expected,f"expected={sorted(expected)} actual={sorted(actual)}"
    if adapter=="artifact_status_integrity":
        bad=[a.get("artifact_id") for a in project.get("artifacts",[]) if a.get("status")=="PASS" and a.get("validation_result") not in {"PASS","NOT_APPLICABLE"}]
        return not bad,f"artifact status escalation={bad}"
    if adapter=="control_evidence_integrity":
        bad=[r.get("control_id") for r in project.get("control_results",[]) if r.get("status")=="PASS" and not valid_control_evidence(r,project)]
        return not bad,f"PASS records with invalid evidence digest/metadata={bad}"
    if adapter=="visual_reference_lock":
        v=project.get("visual",{}); vh=v.get("canonical_reference_hash")
        valid=re.fullmatch("sha256:[a-fA-F0-9]{64}",str(vh or "")) is not None
        signed=any(a.get("role")=="BRAND_OWNER" and a.get("decision")=="APPROVED" and vh in a.get("artifact_hashes",[]) and verify_approval_signature(a,project.get("trusted_signing_keys",{}))[0] for a in project.get("approvals",[]))
        ok=v.get("review_status")=="PASS" and valid and bool(v.get("reviewed_by")) and bool(parse_time(v.get("reviewed_at"))) and signed
        return ok,"visual canonical lock cryptographically verified" if ok else "visual lock requires reviewer, timestamp, PASS, SHA-256 and signed BRAND_OWNER approval"
    raise EngineError(f"No adapter implemented for control {adapter}")

def run_controls(project,project_file,selected=None,now=None):
    results=[]; subject_hash=project_subject_hash(project)
    for cid,adapter,objective in CONTROL_REGISTRY:
        if selected and cid not in selected: continue
        passed,observed=control_check(project,project_file,adapter,now)
        row={"control_id":cid,"test_id":f"TEST-{cid}","objective":objective,"oracle":adapter,"observed":observed,"status":"PASS" if passed else "FAIL","executed_at":utc_now(),"environment":{"python":sys.version.split()[0],"engine":ENGINE_VERSION,"platform":sys.platform},"engine_version":ENGINE_VERSION,"subject_hash":subject_hash}
        row["evidence_hash"]=sha256_json({k:v for k,v in row.items() if k!="evidence_hash"}); results.append(row)
    counts={s:sum(1 for r in results if r["status"]==s) for s in ("PASS","FAIL")}
    return {"report_version":"1.0.0","engine_id":ENGINE_ID,"engine_version":ENGINE_VERSION,"execution_claim":True,"executed_control_count":len(results),"counts":counts,"overall":"PASS" if results and counts["FAIL"]==0 else "FAIL","results":results,"scope_note":"Only the explicit 21-control executable registry is executed. The 1,000 10x10x10 combinations remain candidate definitions, not executable tests."}

def write_report(report,path=None):
    data=json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    if path: path.parent.mkdir(parents=True,exist_ok=True); path.write_text(data,encoding="utf-8")
    else: print(data,end="")

def load_project(path):
    obj=strict_json_load(path)
    if not isinstance(obj,dict): raise EngineError("Project root must be a JSON object")
    return obj

def main(argv=None):
    ap=argparse.ArgumentParser(description="Promkes V4 evidence-contract validator and gate engine")
    sub=ap.add_subparsers(dest="command",required=True)
    val=sub.add_parser("validate",help="Validate project schema and cross-record semantics")
    val.add_argument("project",type=Path); val.add_argument("--schema-dir",type=Path,default=Path("schemas/v4")); val.add_argument("--report",type=Path)
    gate=sub.add_parser("gate",help="Evaluate gates through a target layer")
    gate.add_argument("project",type=Path); gate.add_argument("--target",choices=GATES,default=GATES[-1]); gate.add_argument("--report",type=Path)
    run=sub.add_parser("run-controls",help="Execute all or selected deterministic controls")
    run.add_argument("project",type=Path); run.add_argument("--only",action="append",default=[]); run.add_argument("--report",type=Path); run.add_argument("--updated-project",type=Path)
    inv=sub.add_parser("invalidate",help="List transitive dependents invalidated by an upstream change")
    inv.add_argument("project",type=Path); inv.add_argument("--changed",required=True); inv.add_argument("--report",type=Path)
    args=ap.parse_args(argv)
    try:
        pp=args.project.resolve(); project=load_project(pp)
        if args.command=="validate":
            sd=args.schema_dir.resolve(); errors=schema_validate(project,sd/"project.schema.json")
            for bucket,name in (("claims","claim-record.schema.json"),("scenes","scene-record.schema.json"),("artifacts","artifact-envelope.schema.json"),("capabilities","capability-record.schema.json")):
                for i,row in enumerate(project.get(bucket,[])):
                    for err in schema_validate(row,sd/name): err["path"]=f"$.{bucket}[{i}]"+err["path"][1:]; errors.append(err)
            errors+=semantic_validate(project,pp)
            report={"engine_id":ENGINE_ID,"engine_version":ENGINE_VERSION,"overall":"PASS" if not errors else "FAIL","error_count":len(errors),"errors":errors,"execution_claim":True}
            write_report(report,args.report); return 0 if not errors else 1
        if args.command=="gate":
            report=evaluate_gates(project,pp,args.target); write_report(report,args.report); return 0 if report["overall"]=="PASS" else 2
        if args.command=="run-controls":
            report=run_controls(project,pp,set(args.only) if args.only else None); write_report(report,args.report)
            if args.updated_project:
                updated=dict(project); prior={r.get("control_id"):r for r in project.get("control_results",[])}
                prior.update({r["control_id"]:r for r in report["results"]}); updated["control_results"]=[prior[k] for k in sorted(prior)]
                outroot=args.updated_project.resolve().parent; outroot.mkdir(parents=True,exist_ok=True); payload=[a.get("path") for a in updated.get("assets",[])]+[a.get("content_path") for a in updated.get("artifacts",[])]
                sr=pp.parent
                for rel in sorted({x for x in payload if x}):
                    if not safe_relative_path(rel): raise EngineError(f"Refusing to copy unsafe project payload path: {rel}")
                    source=(sr/PurePosixPath(rel)).resolve()
                    try: source.relative_to(sr.resolve())
                    except ValueError as exc: raise EngineError(f"Project payload escapes source root: {rel}") from exc
                    if source.is_file():
                        dest=outroot/PurePosixPath(rel); dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(source,dest)
                args.updated_project.write_text(json.dumps(updated,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
            return 0 if report["overall"]=="PASS" else 1
        if args.command=="invalidate":
            invalidated=compute_invalidations(project,args.changed); report={"changed_id":args.changed,"invalidated_ids":invalidated,"count":len(invalidated),"execution_claim":True}; write_report(report,args.report); return 0
    except EngineError as exc:
        print(f"ENGINE ERROR: {exc}",file=sys.stderr); return 3
    return 3

if __name__=="__main__": raise SystemExit(main())
