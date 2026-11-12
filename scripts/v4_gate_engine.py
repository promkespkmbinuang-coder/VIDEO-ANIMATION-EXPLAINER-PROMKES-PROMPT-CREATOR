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

import argparse
import copy
import hashlib
import html
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import unquote
from typing import Any, Callable

ENGINE_ID = "promkes-v4-gate-engine"
ENGINE_VERSION = "4.0.0"
ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas" / "v4"

GATE_ORDER = [
    "G0_INTAKE_OK",
    "G1_FACT_LOCK",
    "G2_NARRATIVE_LOCK",
    "G3_VISUAL_LOCK",
    "G4_PROMPT_PREFLIGHT",
    "G5_MANIFEST_VALID",
    "G6_CODE_VALID",
    "G7_RELEASE_APPROVED",
]

CONTROL_IDS = {
    "G0_INTAKE_OK": ["CTRL-INTAKE-INVENTORY", "CTRL-PRIVACY-CLASSIFICATION", "CTRL-RIGHTS-BASIS", "CTRL-UNTRUSTED-INPUTS"],
    "G1_FACT_LOCK": ["CTRL-CLAIM-SCHEMA", "CTRL-SOURCE-PROVENANCE", "CTRL-MATERIAL-CLAIMS", "CTRL-CLINICAL-APPROVAL"],
    "G2_NARRATIVE_LOCK": ["CTRL-NARRATIVE-TRACEABILITY", "CTRL-SAFE-WORDING"],
    "G3_VISUAL_LOCK": ["CTRL-CONTINUITY-LOCKS", "CTRL-VISUAL-REFERENCES"],
    "G4_PROMPT_PREFLIGHT": ["CTRL-PROMPT-INJECTION", "CTRL-PROMPT-BOUNDARY"],
    "G5_MANIFEST_VALID": ["CTRL-SCENE-TIMING", "CTRL-MANIFEST-INTEGRITY"],
    "G6_CODE_VALID": ["CTRL-CAPABILITY-VERIFICATION", "CTRL-CODE-STATIC"],
    "G7_RELEASE_APPROVED": ["CTRL-ARTIFACT-QA", "CTRL-ACCESSIBILITY-QA", "CTRL-RELEASE-APPROVAL"],
}

PASSABLE = {"PASS", "NOT_APPLICABLE"}
FAIL_CLOSED = {"NOT_RUN", "NOT_VERIFIED", "BLOCKED", "STALE", "INVALIDATED", "PARTIAL", "IN_PROGRESS", "NOT_STARTED"}
CLAIM_BLOCKING = {"UNVERIFIED", "CONTRADICTED", "UNKNOWN", "STALE"}
MATERIAL_CLAIM_TYPES = {"PREVENTION", "TREATMENT", "RISK", "STATISTIC", "CAUSAL"}
PRIVACY_CLASSES = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "SENSITIVE"}
RIGHTS_STATES = {"CLEARED", "RESTRICTED", "PENDING", "UNKNOWN", "NOT_APPLICABLE"}

INJECTION_PATTERNS = [
    re.compile(r"(ignore|disregard|forget|bypass|override)\s+(all\s+)?(the\s+)?(previous|prior|above|earlier)\s+(system\s+|developer\s+)?instructions?", re.I),
    re.compile(r"(reveal|show|print|expose|dump)\s+(the\s+)?(hidden\s+)?(system|developer|internal)\s+prompt", re.I),
    re.compile(r"(show|reveal|print|expose)\s+(me\s+)?hidden\s+instructions", re.I),
    re.compile(r"(exfiltrat(e|ion)|send|forward|upload|post)\s+(all\s+)?(the\s+)?(secrets|credentials|api\s+keys|tokens|passwords)", re.I),
    re.compile(r"(disable|override|bypass|suspend)\s+(the\s+)?(safety|security|content)\s+(policy|rules?|guardrails?)", re.I),
    re.compile(r"(act\s+as|become|switch\s+to)\s+(an?\s+)?(dan|jailbreak|unrestricted|unfiltered)\b", re.I),
    re.compile(r"you\s+are\s+now\s+.*(not\s+bound|no\s+restrictions|ignore\s+policy)", re.I),
    re.compile(r"(call|invoke|use)\s+(the\s+)?(browser|tool|function)(\s+tool)?\s+and\s+(send|upload|exfiltrate)", re.I),
]


def normalize_prompt_text(value: str) -> str:
    """Normalize common obfuscation before applying heuristic injection patterns."""
    text = unicodedata.normalize("NFKC", html.unescape(value))
    text = unquote(text)
    text = re.sub(r"[\u200b-\u200f\u2060\ufeff]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def detect_prompt_injection(value: str) -> list[str]:
    """Return matched heuristic pattern labels; absence of a match is not proof of safety."""
    normalized = normalize_prompt_text(value)
    return [pattern.pattern for pattern in INJECTION_PATTERNS if pattern.search(normalized)]



def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _normalize(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if isinstance(value, dict):
        return {unicodedata.normalize("NFC", str(k)): _normalize(v) for k, v in value.items()}
    return value


def canonical_json_bytes(value: Any) -> bytes:
    """Canonical UTF-8 JSON: NFC strings, LF newlines, sorted keys, no whitespace."""
    normalized = _normalize(value)
    return json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def content_hash(value: Any, *, exclude: tuple[str, ...] = ("content_hash",)) -> str:
    payload = dict(value) if isinstance(value, dict) else value
    if isinstance(payload, dict):
        for key in exclude:
            payload.pop(key, None)
    return "sha256:" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def sha256_bytes(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"sha256:[0-9a-fA-F]{64}", value) is not None


def safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip() or "\\" in value or "\x00" in value:
        return False
    if re.match(r"^[A-Za-z]:", value) or value.startswith(("/", "~")):
        return False
    parts = PurePosixPath(value).parts
    return bool(parts) and all(p not in {"", ".", ".."} for p in parts)


def _schema_validator(kind: str):
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

def validate_record(record: dict[str, Any], kind: str) -> list[str]:
    """Validate one claim/artifact envelope against its versioned JSON Schema.

    This public helper is shared by CLI paths and tests. It deliberately performs
    structural validation only; semantic and human approval checks remain owned
    by project validation and the sequential gates.
    """
    if not isinstance(record, dict):
        return ["Record must be a JSON object"]
    allowed = {"project", "claim-record", "scene-record", "capability-record", "artifact-envelope"}
    if kind not in allowed:
        return [f"Unknown record schema kind: {kind}"]
    schema_path = SCHEMA_DIR / f"{kind}.schema.json"
    if not schema_path.is_file():
        return [f"Schema file not found: {schema_path}"]
    return [
        f"{error['path']}: {error['message']}"
        for error in schema_validate(record, schema_path)
    ]

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

def _out(control_id: str, status: str, reason: str, observed: Any = None, evidence: list[str] | None = None) -> dict[str, Any]:
    return {
        "control_id": control_id,
        "status": status,
        "reason": reason,
        "observed": observed,
        "oracle": "deterministic-v4-gate-engine",
        "executed_at": utc_now(),
        "environment": {"python": sys.version.split()[0], "engine": ENGINE_VERSION},
        "evidence_refs": evidence or [],
    }


def _missing(control_id: str, field: str) -> dict[str, Any]:
    return _out(control_id, "NOT_RUN", f"Required input '{field}' is absent or incomplete")


def _evidence_refs(value: Any) -> list[str]:
    return [x for x in value if isinstance(x, str) and x.strip()] if isinstance(value, list) else []


def _valid_approval(project: dict[str, Any], domain: str, role: str, hashes: set[str] | None = None, approver_ids: set[str] | None = None) -> tuple[bool, str, list[str]]:
    registry = {x.get("approver_id"): x for x in project.get("approver_registry", []) if isinstance(x, dict)}
    for approval in project.get("approvals", []):
        if not isinstance(approval, dict) or approval.get("status") == "INVALIDATED" or approval.get("domain") != domain or approval.get("decision") != "APPROVED":
            continue
        approver_id = approval.get("approver_id")
        if approver_ids and approver_id not in approver_ids:
            continue
        identity = registry.get(approver_id)
        if not identity or identity.get("active") is not True or role not in identity.get("roles", []):
            continue
        if not identity.get("authority_evidence_ref") or not approval.get("approved_at"):
            continue
        if not approval.get("signature_evidence_ref"):
            continue
        bound = set(approval.get("artifact_hashes", []))
        if hashes and not hashes.issubset(bound):
            continue
        refs = [identity["authority_evidence_ref"], approval["signature_evidence_ref"]]
        refs.extend(_evidence_refs(approval.get("evidence_refs")))
        return True, f"{domain} approval structurally matches active approver registry", refs
    return False, f"No hash-bound {domain} approval from an active approver with required role {role}", []


def _source_map(project: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {x.get("source_id"): x for x in project.get("sources", []) if isinstance(x, dict) and x.get("source_id")}


def _claim_map(project: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {x.get("claim_id"): x for x in project.get("claims", []) if isinstance(x, dict) and x.get("claim_id")}


def _control(project: dict[str, Any], control_id: str) -> dict[str, Any]:
    """Run one named deterministic control and return an auditable observation."""
    if control_id == "CTRL-INTAKE-INVENTORY":
        intake = project.get("intake")
        inputs = intake.get("inputs") if isinstance(intake, dict) else None
        if not isinstance(inputs, list) or not inputs:
            return _missing(control_id, "intake.inputs")
        bad = [i for i, x in enumerate(inputs) if not isinstance(x, dict) or not all(x.get(k) for k in ("input_id", "input_type", "origin"))]
        if bad:
            return _out(control_id, "FAIL", "Each intake input needs input_id, input_type and origin", {"invalid_indexes": bad})
        return _out(control_id, "PASS", "All intake inputs are inventoried", {"count": len(inputs)}, [f"engine://{control_id}/inventory"])

    if control_id == "CTRL-PRIVACY-CLASSIFICATION":
        value = project.get("privacy_classification")
        if value not in PRIVACY_CLASSES:
            return _out(control_id, "BLOCKED", "Project privacy classification is missing or UNKNOWN", {"privacy_classification": value})
        return _out(control_id, "PASS", "Privacy classification uses a controlled value", {"privacy_classification": value}, [f"engine://{control_id}/classification"])

    if control_id == "CTRL-RIGHTS-BASIS":
        rights = project.get("rights", {})
        state = rights.get("status") if isinstance(rights, dict) else None
        refs = _evidence_refs(rights.get("evidence_refs")) if isinstance(rights, dict) else []
        rationale = rights.get("not_applicable_rationale") if isinstance(rights, dict) else None
        if state == "NOT_APPLICABLE":
            if rationale:
                return _out(control_id, "NOT_APPLICABLE", rationale, {"status": state})
            return _out(control_id, "FAIL", "NOT_APPLICABLE rights status requires a rationale", {"status": state})
        if state != "CLEARED" or not refs:
            return _out(control_id, "BLOCKED", "Rights must be CLEARED with evidence refs before production", {"status": state, "evidence_refs": refs})
        return _out(control_id, "PASS", "Rights status is CLEARED with recorded evidence references", {"status": state}, refs)

    if control_id == "CTRL-UNTRUSTED-INPUTS":
        items = project.get("untrusted_inputs")
        if not isinstance(items, list):
            return _missing(control_id, "untrusted_inputs")
        if not items:
            rationale = project.get("no_untrusted_inputs_rationale")
            if rationale:
                return _out(control_id, "NOT_APPLICABLE", rationale)
            return _out(control_id, "BLOCKED", "Empty untrusted_inputs requires explicit rationale")
        invalid = []
        base = Path(project.get("project_root", ROOT)).resolve()
        for i, item in enumerate(items):
            if not isinstance(item, dict) or not item.get("origin") or not is_sha256(item.get("content_hash")) or item.get("delimited") is not True or item.get("treat_as_data") is not True:
                invalid.append(i)
                continue
            observed_hash = None
            if isinstance(item.get("content"), str):
                observed_hash = sha256_bytes(item["content"].encode("utf-8"))
            elif safe_relative_path(item.get("snapshot_path")):
                snapshot = (base / item["snapshot_path"]).resolve()
                try:
                    snapshot.relative_to(base)
                except ValueError:
                    invalid.append(i)
                    continue
                if snapshot.is_file():
                    observed_hash = sha256_bytes(snapshot.read_bytes())
            if observed_hash != item["content_hash"]:
                invalid.append(i)
        if invalid:
            return _out(control_id, "FAIL", "Untrusted inputs must carry origin, byte-verifiable SHA-256, explicit delimiting and data-only treatment", {"invalid_indexes": invalid})
        return _out(control_id, "PASS", "All untrusted inputs are provenance-tagged and isolated as data", {"count": len(items)}, [f"engine://{control_id}/inventory"])

    if control_id == "CTRL-CLAIM-SCHEMA":
        claims = project.get("claims")
        if not isinstance(claims, list) or not claims:
            return _missing(control_id, "claims")
        all_errors = []
        for claim in claims:
            if not isinstance(claim, dict):
                all_errors.append("claim entry is not an object")
                continue
            all_errors.extend(f"{claim.get('claim_id', '<missing>')}: {e}" for e in validate_record(claim, "claim-record"))
        if all_errors:
            return _out(control_id, "FAIL", "One or more claim records violate the schema or semantic contract", {"errors": all_errors})
        return _out(control_id, "PASS", "All claim records satisfy schema and semantic constraints", {"count": len(claims)}, [f"engine://{control_id}/schema-validation"])

    if control_id == "CTRL-SOURCE-PROVENANCE":
        claims = project.get("claims")
        sources = _source_map(project)
        if not isinstance(claims, list) or not claims:
            return _missing(control_id, "claims")
        missing = []
        malformed = []
        for claim in claims:
            if not isinstance(claim, dict):
                continue
            for sid in claim.get("source_ids", []):
                source = sources.get(sid)
                if not source:
                    missing.append(sid)
                elif not source.get("source_uri") or not source.get("retrieved_at") or not is_sha256(source.get("source_hash")):
                    malformed.append(sid)
                elif source.get("source_hash") not in claim.get("source_hashes", []):
                    malformed.append(sid)
                elif isinstance(source.get("snapshot_text"), str):
                    if sha256_bytes(source["snapshot_text"].encode("utf-8")) != source["source_hash"]:
                        malformed.append(sid)
                elif source.get("snapshot_path"):
                    base = Path(project.get("project_root", ROOT)).resolve()
                    p = (base / source["snapshot_path"]).resolve()
                    try:
                        p.relative_to(base)
                    except ValueError:
                        malformed.append(sid)
                        continue
                    if not p.is_file() or sha256_bytes(p.read_bytes()) != source["source_hash"]:
                        malformed.append(sid)
                else:
                    malformed.append(sid)
        if missing or malformed:
            return _out(control_id, "FAIL", "Source references are missing or provenance metadata/hash is invalid", {"missing_source_ids": sorted(set(missing)), "invalid_source_ids": sorted(set(malformed))})
        return _out(control_id, "PASS", "All claim source references resolve to provenance records", {"source_count": len(sources)}, [f"engine://{control_id}/provenance-check"])

    if control_id == "CTRL-MATERIAL-CLAIMS":
        claims = project.get("claims")
        if not isinstance(claims, list) or not claims:
            return _missing(control_id, "claims")
        blocked = [x.get("claim_id") for x in claims if isinstance(x, dict) and (x.get("status") in CLAIM_BLOCKING or x.get("evidence_level") == "UNVERIFIED")]
        partial = [x.get("claim_id") for x in claims if isinstance(x, dict) and x.get("status") in {"PARTIALLY_SUPPORTED", "MIXED"}]
        if blocked:
            return _out(control_id, "BLOCKED", "Material unverified, contradicted, unknown or stale claims prevent Fact Lock", {"blocked_claim_ids": blocked})
        if partial:
            held = [x.get("claim_id") for x in claims if isinstance(x, dict) and x.get("status") in {"PARTIALLY_SUPPORTED", "MIXED"} and not x.get("allowed_wording")]
            if held:
                return _out(control_id, "BLOCKED", "Partially supported or mixed claims require constrained allowed_wording", {"claim_ids": held})
        return _out(control_id, "PASS", "No claim is in a fail-closed evidence state", {"claim_count": len(claims)}, [f"engine://{control_id}/claim-ledger"])

    if control_id == "CTRL-CLINICAL-APPROVAL":
        claims = project.get("claims", [])
        material = [c for c in claims if isinstance(c, dict) and c.get("claim_type") in MATERIAL_CLAIM_TYPES]
        if not material:
            rationale = project.get("no_material_health_claims_rationale")
            return _out(control_id, "NOT_APPLICABLE", rationale, {"material_claims": 0}) if rationale else _out(control_id, "BLOCKED", "No material health claims found; explicit N/A rationale is required")
        unreviewed = [c.get("claim_id") for c in material if c.get("reviewed_by_human") is not True or c.get("reviewer_role") != "CLINICIAN" or not c.get("reviewer_id") or not c.get("reviewed_at")]
        if unreviewed:
            return _out(control_id, "BLOCKED", "Every material health claim requires a named clinical review record", {"claim_ids": unreviewed})
        approval_refs = []
        missing_claims = []
        for claim in material:
            claim_hashes = {h for h in claim.get("source_hashes", []) if is_sha256(h)}
            reviewer_ids = {claim.get("reviewer_id")} if claim.get("reviewer_id") else set()
            ok, reason, refs = _valid_approval(project, "CLINICAL", "CLINICIAN", claim_hashes, reviewer_ids)
            if not ok:
                missing_claims.append(claim.get("claim_id"))
            else:
                approval_refs.extend(refs)
        if missing_claims:
            return _out(control_id, "BLOCKED", "Every material claim must have its own reviewer-matched, source-hash-bound clinical approval", {"claim_ids": missing_claims})
        return _out(control_id, "PASS", "Every material claim has a reviewer-matched, source-hash-bound clinical approval", {"reviewed_claims": len(material)}, sorted(set(approval_refs)))

    if control_id == "CTRL-NARRATIVE-TRACEABILITY":
        lines = project.get("narrative_lines")
        claims = _claim_map(project)
        if not isinstance(lines, list) or not lines:
            return _missing(control_id, "narrative_lines")
        problems = []
        for i, line in enumerate(lines):
            if not isinstance(line, dict) or not isinstance(line.get("claim_refs"), list) or not line.get("claim_refs"):
                problems.append(f"line[{i}] has no claim_refs")
            elif any(cid not in claims for cid in line["claim_refs"]):
                problems.append(f"line[{i}] references unknown claims")
        if problems:
            return _out(control_id, "FAIL", "Narrative lines must trace to known claim IDs", {"problems": problems})
        return _out(control_id, "PASS", "Every narrative line is traceable to the claim ledger", {"line_count": len(lines)}, [f"engine://{control_id}/traceability"])

    if control_id == "CTRL-SAFE-WORDING":
        lines = project.get("narrative_lines")
        claims = _claim_map(project)
        if not isinstance(lines, list) or not lines:
            return _missing(control_id, "narrative_lines")
        problems = []
        for i, line in enumerate(lines):
            if not isinstance(line, dict):
                problems.append(f"line[{i}] is not an object")
                continue
            text = re.sub(r"\s+", " ", str(line.get("text", "")).strip()).casefold()
            for cid in line.get("claim_refs", []):
                claim = claims.get(cid, {})
                allowed = [re.sub(r"\s+", " ", str(x).strip()).casefold() for x in claim.get("allowed_wording", [])]
                forbidden = [re.sub(r"\s+", " ", str(x).strip()).casefold() for x in claim.get("forbidden_wording", [])]
                if any(term and term in text for term in forbidden):
                    problems.append(f"line[{i}] contains forbidden wording for {cid}")
                if not allowed or not any(text == phrase for phrase in allowed):
                    problems.append(f"line[{i}] does not exactly match an allowed phrase for {cid}")
        if problems:
            return _out(control_id, "BLOCKED", "Narrative wording exceeds or deviates from claim-approved wording", {"problems": problems})
        return _out(control_id, "PASS", "All narrative claim wording matches an approved phrase exactly", {"line_count": len(lines)}, [f"engine://{control_id}/wording-check"])

    if control_id == "CTRL-CONTINUITY-LOCKS":
        lock = project.get("continuity_lock")
        if not isinstance(lock, dict):
            return _missing(control_id, "continuity_lock")
        if lock.get("status") != "LOCKED" or not lock.get("canon_version") or not is_sha256(lock.get("content_hash")) or not _evidence_refs(lock.get("evidence_refs")):
            return _out(control_id, "BLOCKED", "Continuity lock requires LOCKED status, version, SHA-256 and evidence", {"status": lock.get("status")})
        return _out(control_id, "PASS", "Continuity canon is hash-locked", {"canon_version": lock["canon_version"]}, _evidence_refs(lock.get("evidence_refs")))

    if control_id == "CTRL-VISUAL-REFERENCES":
        scenes = project.get("scenes")
        refs = {r.get("reference_id") for r in project.get("reference_assets", []) if isinstance(r, dict) and r.get("reference_id")}
        if not isinstance(scenes, list) or not scenes:
            return _missing(control_id, "scenes")
        missing = []
        for scene in scenes:
            ids = scene.get("reference_ids", []) if isinstance(scene, dict) else []
            if not ids or any(x not in refs for x in ids):
                missing.append(scene.get("scene_id", "<unknown>") if isinstance(scene, dict) else "<invalid>")
        if missing:
            return _out(control_id, "BLOCKED", "Every scene requires resolvable visual reference IDs", {"scene_ids": missing})
        return _out(control_id, "PASS", "All scene reference IDs resolve", {"scene_count": len(scenes)}, [f"engine://{control_id}/reference-index"])

    if control_id == "CTRL-PROMPT-INJECTION":
        prompts = project.get("prompts")
        if not isinstance(prompts, list) or not prompts:
            return _missing(control_id, "prompts")
        hits = []
        for i, item in enumerate(prompts):
            if not isinstance(item, dict):
                hits.append(f"prompt[{i}] is not an object")
                continue
            body = str(item.get("trusted_instructions", ""))
            for pattern_label in detect_prompt_injection(body):
                hits.append(f"prompt[{i}] matched heuristic {pattern_label}")
        if hits:
            return _out(control_id, "BLOCKED", "Potential instruction-smuggling text detected in trusted instruction area; heuristic requires human inspection", {"hits": hits})
        return _out(control_id, "PASS", "No configured injection heuristic matched trusted instruction fields (not a proof of safety)", {"prompt_count": len(prompts)}, [f"engine://{control_id}/heuristic-scan"])

    if control_id == "CTRL-PROMPT-BOUNDARY":
        prompts = project.get("prompts")
        if not isinstance(prompts, list) or not prompts:
            return _missing(control_id, "prompts")
        bad = []
        for i, item in enumerate(prompts):
            if not isinstance(item, dict):
                bad.append(i)
            elif item.get("untrusted_payloads") and (item.get("boundary_markers") != ["<UNTRUSTED_SOURCE>", "</UNTRUSTED_SOURCE>"] or item.get("treat_payload_as_data") is not True):
                bad.append(i)
        if bad:
            return _out(control_id, "FAIL", "Untrusted prompt payloads need canonical delimiters and data-only instruction", {"prompt_indexes": bad})
        return _out(control_id, "PASS", "Prompt records preserve trusted/untrusted instruction boundaries", {"prompt_count": len(prompts)}, [f"engine://{control_id}/boundary-check"])

    if control_id == "CTRL-SCENE-TIMING":
        scenes = project.get("scenes")
        if not isinstance(scenes, list) or not scenes:
            return _missing(control_id, "scenes")
        errors = [f"scene[{i}] is not an object" for i, scene in enumerate(scenes) if not isinstance(scene, dict)]
        rows = sorted((x for x in scenes if isinstance(x, dict)), key=lambda x: (x.get("order", -1), x.get("start_frame", -1)))
        fps_values = set()
        for i, scene in enumerate(rows):
            start, end, fps = scene.get("start_frame"), scene.get("end_frame"), scene.get("fps")
            if isinstance(start, bool) or isinstance(end, bool) or isinstance(fps, bool) or not isinstance(start, int) or not isinstance(end, int) or not isinstance(fps, (int, float)) or start < 0 or end <= start or fps <= 0:
                errors.append(f"scene {scene.get('scene_id', i)} has invalid frame/fps values")
            if isinstance(fps, (int, float)):
                fps_values.add(fps)
            if i == 0 and start != 0:
                errors.append("first scene must start at frame 0")
            if i > 0:
                previous = rows[i - 1]
                if isinstance(previous, dict) and isinstance(start, int) and isinstance(previous.get("end_frame"), int):
                    if start != previous["end_frame"]:
                        errors.append(f"gap or overlap between {previous.get('scene_id')} and {scene.get('scene_id')}")
        if len(fps_values) > 1:
            errors.append("all scenes must use one project fps/timebase")
        if errors:
            return _out(control_id, "FAIL", "Scene timing arithmetic is invalid", {"errors": errors})
        return _out(control_id, "PASS", "Scene frame ranges are contiguous, positive and use one fps", {"scene_count": len(rows), "fps": next(iter(fps_values))}, [f"engine://{control_id}/timing-validation"])

    if control_id == "CTRL-MANIFEST-INTEGRITY":
        manifest = project.get("manifest")
        if not isinstance(manifest, dict):
            return _missing(control_id, "manifest")
        errors = validate_record(manifest, "artifact-envelope")
        paths = manifest.get("asset_paths", [])
        unsafe = [p for p in paths if not safe_relative_path(p)]
        if unsafe:
            errors.append(f"unsafe asset paths: {unsafe}")
        if errors:
            return _out(control_id, "FAIL", "Manifest schema/hash/path validation failed", {"errors": errors})
        return _out(control_id, "PASS", "Manifest contract, canonical hash and asset paths validate", {"asset_count": len(paths)}, [f"engine://{control_id}/manifest-validation"])

    if control_id == "CTRL-CAPABILITY-VERIFICATION":
        renderer = project.get("renderer")
        if not isinstance(renderer, dict) or renderer.get("requested") is not True:
            rationale = renderer.get("not_requested_rationale") if isinstance(renderer, dict) else None
            return _out(control_id, "NOT_APPLICABLE", rationale, {"renderer_requested": False}) if rationale else _out(control_id, "BLOCKED", "Renderer not requested requires explicit N/A rationale")
        capability = next((x for x in project.get("capabilities", []) if isinstance(x, dict) and x.get("operation") == "render" and x.get("provider") == renderer.get("provider") and x.get("target") == renderer.get("target") and x.get("version") == renderer.get("version")), None)
        if not capability or capability.get("status") != "VERIFIED" or not capability.get("checked_at") or not _evidence_refs(capability.get("evidence_refs")):
            return _out(control_id, "BLOCKED", "Exact renderer/provider/version capability lacks VERIFIED status and evidence", {"renderer": renderer, "capability": capability})
        return _out(control_id, "PASS", "Exact renderer operation and version have recorded capability evidence", {"provider": renderer["provider"], "target": renderer["target"], "version": renderer["version"]}, _evidence_refs(capability.get("evidence_refs")))

    if control_id == "CTRL-CODE-STATIC":
        checks = project.get("code_checks")
        if not isinstance(checks, list) or not checks:
            return _missing(control_id, "code_checks")
        bad = [i for i, c in enumerate(checks) if not isinstance(c, dict) or c.get("status") != "PASS" or not c.get("test_id") or not c.get("command") or not c.get("executed_at") or not c.get("environment") or not _evidence_refs(c.get("evidence_refs"))]
        if bad:
            return _out(control_id, "BLOCKED", "Every static code check needs PASS, test_id and evidence refs", {"invalid_indexes": bad})
        return _out(control_id, "PASS", "All declared static code checks have evidence", {"check_count": len(checks)}, [f"engine://{control_id}/code-check-ledger"])

    if control_id == "CTRL-ARTIFACT-QA":
        artifacts = project.get("rendered_artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            return _missing(control_id, "rendered_artifacts")
        bad = []
        for i, art in enumerate(artifacts):
            if not isinstance(art, dict) or not safe_relative_path(art.get("path")) or not is_sha256(art.get("sha256")) or art.get("inspected") is not True or art.get("qa_status") != "PASS" or not _evidence_refs(art.get("qa_evidence_refs")):
                bad.append(i)
                continue
            base = Path(project.get("project_root", ROOT)).resolve()
            p = (base / art["path"]).resolve()
            try:
                p.relative_to(base)
            except ValueError:
                bad.append(i)
                continue
            if not p.is_file() or sha256_bytes(p.read_bytes()) != art["sha256"]:
                bad.append(i)
        if bad:
            return _out(control_id, "BLOCKED", "Every rendered artifact needs a real in-root file, matching hash and inspectable QA evidence", {"invalid_indexes": bad})
        return _out(control_id, "PASS", "Rendered artifact hashes and QA records match local files", {"artifact_count": len(artifacts)}, [f"engine://{control_id}/artifact-qa"])

    if control_id == "CTRL-ACCESSIBILITY-QA":
        qa = project.get("accessibility_qa")
        if not isinstance(qa, dict) or not qa.get("standard"):
            return _missing(control_id, "accessibility_qa.standard")
        if qa.get("status") != "PASS" or not qa.get("scope") or not _evidence_refs(qa.get("evidence_refs")):
            return _out(control_id, "BLOCKED", "Accessibility QA needs named standard, scope, PASS and evidence refs", {"status": qa.get("status")})
        ok, reason, approval_refs = _valid_approval(project, "ACCESSIBILITY", "ACCESSIBILITY_REVIEWER")
        if not ok:
            return _out(control_id, "BLOCKED", reason, {"standard": qa["standard"], "scope": qa["scope"]})
        return _out(control_id, "PASS", "Accessibility QA and authorized reviewer record are evidence-linked", {"standard": qa["standard"], "scope": qa["scope"]}, _evidence_refs(qa.get("evidence_refs")) + approval_refs)

    if control_id == "CTRL-RELEASE-APPROVAL":
        hashes = {a.get("sha256") for a in project.get("rendered_artifacts", []) if isinstance(a, dict) and is_sha256(a.get("sha256"))}
        ok, reason, refs = _valid_approval(project, "RELEASE", "PRODUCER", hashes if hashes else None)
        if not ok:
            return _out(control_id, "BLOCKED", reason)
        return _out(control_id, "PASS", reason, {"hashes_bound": sorted(hashes)}, refs)

    return _out(control_id, "NOT_VERIFIED", "No evaluator is registered for this control ID")


def evaluate_project(project: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(project, dict):
        raise ValueError("Project input must be a JSON object")
    gate_results: list[dict[str, Any]] = []
    prior_status = "PASS"
    for gate_id in GATE_ORDER:
        control_results = []
        if prior_status != "PASS":
            gate_results.append({"gate_id": gate_id, "status": "BLOCKED", "reason": f"Predecessor gate did not PASS (status={prior_status})", "controls": []})
            prior_status = "BLOCKED"
            continue
        for control_id in CONTROL_IDS[gate_id]:
            control_results.append(_control(project, control_id))
        failing = [x for x in control_results if x["status"] == "FAIL"]
        blocked = [x for x in control_results if x["status"] == "BLOCKED"]
        unrun = [x for x in control_results if x["status"] in FAIL_CLOSED]
        invalid_na = [x for x in control_results if x["status"] == "NOT_APPLICABLE" and not x.get("reason")]
        if failing:
            status, reason = "FAIL", "One or more required controls failed"
        elif blocked:
            status, reason = "BLOCKED", "One or more required controls are blocked"
        elif unrun:
            status, reason = "NOT_RUN", "One or more required controls have not been executed or verified"
        elif invalid_na:
            status, reason = "FAIL", "NOT_APPLICABLE control has no rationale"
        elif all(x["status"] in PASSABLE for x in control_results):
            status, reason = "PASS", "All required controls passed or were explicitly not applicable with rationale"
        else:
            status, reason = "NOT_VERIFIED", "Gate status could not be established"
        gate_results.append({"gate_id": gate_id, "status": status, "reason": reason, "controls": control_results})
        prior_status = status
    all_pass = all(x["status"] == "PASS" for x in gate_results)
    return {
        "engine_id": ENGINE_ID,
        "engine_version": ENGINE_VERSION,
        "project_id": project.get("project_id"),
        "evaluated_at": utc_now(),
        "policy": "FAIL_CLOSED",
        "release_eligible": all_pass,
        "overall_status": "PASS" if all_pass else next((x["status"] for x in gate_results if x["status"] != "PASS"), "NOT_VERIFIED"),
        "gates": gate_results,
        "summary": {
            "gate_count": len(gate_results),
            "passed": sum(x["status"] == "PASS" for x in gate_results),
            "failed": sum(x["status"] == "FAIL" for x in gate_results),
            "blocked": sum(x["status"] == "BLOCKED" for x in gate_results),
            "not_run_or_unverified": sum(x["status"] in {"NOT_RUN", "NOT_VERIFIED", "IN_PROGRESS", "NOT_STARTED", "PARTIAL"} for x in gate_results),
        },
        "limitations": [
            "Structural approval records do not independently authenticate a person's identity or credentials.",
            "Prompt-injection scanning is heuristic and cannot prove prompt safety or model behavior.",
            "A PASS only covers controls evaluated by this engine against supplied data and evidence references.",
            "Live ChatGPT invocation, external AI/ASR/diarization, renderer runtime and media QA require separate real execution evidence.",
        ],
    }


def validate_dependency_graph(records: list[dict[str, Any]]) -> list[str]:
    errors = []
    ids = [x.get("artifact_id") for x in records if isinstance(x, dict)]
    if len(ids) != len(set(ids)):
        errors.append("duplicate artifact_id in dependency graph")
    known = set(ids)
    graph: dict[str, list[str]] = {}
    for item in records:
        if not isinstance(item, dict) or not item.get("artifact_id"):
            errors.append("dependency record missing artifact_id")
            continue
        deps = item.get("depends_on", [])
        if not isinstance(deps, list):
            errors.append(f"depends_on must be a list for {item['artifact_id']}")
            continue
        missing = [x for x in deps if x not in known]
        if missing:
            errors.append(f"unknown dependencies for {item['artifact_id']}: {missing}")
        graph[item["artifact_id"]] = deps
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for dep in graph.get(node, []):
            if dep in graph and visit(dep):
                return True
        visiting.remove(node)
        visited.add(node)
        return False
    for node in graph:
        if visit(node):
            errors.append("dependency graph contains a cycle")
            break
    return errors


def invalidation_plan(records: list[dict[str, Any]], changed_ids: list[str]) -> list[str]:
    errors = validate_dependency_graph(records)
    if errors:
        raise ValueError("; ".join(errors))
    known = {x["artifact_id"] for x in records}
    unknown = sorted(set(changed_ids) - known)
    if unknown:
        raise ValueError(f"Unknown changed artifact IDs: {unknown}")
    dependents: dict[str, set[str]] = {x: set() for x in known}
    for item in records:
        for dep in item.get("depends_on", []):
            dependents[dep].add(item["artifact_id"])
    invalidated = set()
    frontier = list(changed_ids)
    while frontier:
        node = frontier.pop()
        for child in dependents[node]:
            if child not in invalidated and child not in changed_ids:
                invalidated.add(child)
                frontier.append(child)
    return sorted(invalidated)


def apply_invalidation(project: dict[str, Any], changed_ids: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return a revised project snapshot with transitive dependents invalidated.

    This function never mutates the input project. The caller must write the
    returned snapshot to a distinct output path. Every affected artifact needs
    a versioned artifact envelope so its status and hash can be updated.
    """
    if not isinstance(project, dict):
        raise ValueError("Project input must be a JSON object")
    graph = project.get("dependency_graph")
    if not isinstance(graph, list):
        raise ValueError("dependency_graph is required")
    invalidated_ids = invalidation_plan(graph, changed_ids)

    records = project.get("artifact_records")
    if not isinstance(records, list):
        raise ValueError("artifact_records is required to apply invalidation; use invalidation-plan for plan-only output")
    record_ids = [x.get("artifact_id") for x in records if isinstance(x, dict)]
    if len(record_ids) != len(records) or len(record_ids) != len(set(record_ids)):
        raise ValueError("artifact_records must contain objects with unique artifact_id values")
    missing = sorted(set(invalidated_ids) - set(record_ids))
    if missing:
        raise ValueError(f"Cannot apply invalidation; artifact envelopes are missing for: {missing}")

    revised = copy.deepcopy(project)
    record_index = {x["artifact_id"]: x for x in revised["artifact_records"]}
    previous_hashes: set[str] = set()
    now = utc_now()

    for artifact_id in invalidated_ids:
        record = record_index[artifact_id]
        previous_hash = record.get("content_hash")
        if is_sha256(previous_hash):
            previous_hashes.add(previous_hash)
        record["status"] = "INVALIDATED"
        record["validation_result"] = "NOT_RUN"
        record["invalidated_by"] = ",".join(sorted(set(changed_ids)))
        record["updated_at"] = now
        record["content_hash"] = content_hash(record)
        errors = validate_record(record, "artifact-envelope")
        if errors:
            raise ValueError(f"Invalidated artifact envelope {artifact_id} failed schema/hash validation: {errors}")

    for node in revised.get("dependency_graph", []):
        if isinstance(node, dict) and node.get("artifact_id") in invalidated_ids:
            node["status"] = "INVALIDATED"

    invalidated_approvals = 0
    for approval in revised.get("approvals", []):
        if not isinstance(approval, dict) or approval.get("status") == "INVALIDATED":
            continue
        bound_hashes = set(approval.get("artifact_hashes", []))
        if previous_hashes.intersection(bound_hashes):
            approval["status"] = "INVALIDATED"
            approval["invalidated_at"] = now
            approval["invalidated_by_artifact_ids"] = invalidated_ids
            invalidated_approvals += 1

    event_payload = {
        "event_type": "DEPENDENCY_INVALIDATION",
        "project_id": revised.get("project_id"),
        "changed_artifact_ids": sorted(set(changed_ids)),
        "invalidated_artifact_ids": invalidated_ids,
        "previous_artifact_hashes": sorted(previous_hashes),
        "invalidated_approval_count": invalidated_approvals,
        "source_project_hash": content_hash(project),
        "engine_version": ENGINE_VERSION,
        "created_at": now,
    }
    event = dict(event_payload)
    event["event_id"] = "INV-" + content_hash(event_payload).split(":", 1)[1][:20]
    revised.setdefault("invalidation_events", []).append(event)
    revised["last_invalidation_event_id"] = event["event_id"]
    return revised, event


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command, kind in (("validate-claim", "claim-record"), ("validate-artifact", "artifact-envelope")):
        p = sub.add_parser(command)
        p.add_argument("--input", required=True, type=Path)
    p = sub.add_parser("evaluate")
    p.add_argument("--project", required=True, type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--require-release", action="store_true", help="Exit non-zero unless all eight gates PASS")
    p = sub.add_parser("invalidation-plan")
    p.add_argument("--project", required=True, type=Path)
    p.add_argument("--changed", required=True, nargs="+")
    p.add_argument("--output", type=Path)
    p = sub.add_parser("apply-invalidation")
    p.add_argument("--project", required=True, type=Path)
    p.add_argument("--changed", required=True, nargs="+")
    p.add_argument("--output", required=True, type=Path)
    p = sub.add_parser("hash")
    p.add_argument("--input", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command in {"validate-claim", "validate-artifact"}:
            kind = "claim-record" if args.command == "validate-claim" else "artifact-envelope"
            record = _load_json(args.input)
            errors = validate_record(record, kind)
            if errors:
                print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
                return 1
            print(json.dumps({"status": "PASS", "kind": kind, "engine_version": ENGINE_VERSION}, indent=2))
            return 0
        if args.command == "evaluate":
            report = evaluate_project(_load_json(args.project))
            if args.output:
                _write_json(args.output, report)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 1 if args.require_release and not report["release_eligible"] else 0
        if args.command == "invalidation-plan":
            project = _load_json(args.project)
            items = project.get("dependency_graph", [])
            plan = {"changed": args.changed, "invalidated_dependents": invalidation_plan(items, args.changed), "status": "PLAN_ONLY_NO_MUTATION"}
            if args.output:
                _write_json(args.output, plan)
            print(json.dumps(plan, indent=2))
            return 0
        if args.command == "apply-invalidation":
            if args.output.resolve() == args.project.resolve():
                raise ValueError("apply-invalidation requires a new output path; the input project is never overwritten")
            revised, event = apply_invalidation(_load_json(args.project), args.changed)
            _write_json(args.output, revised)
            print(json.dumps({
                "status": "INVALIDATION_APPLIED_TO_NEW_SNAPSHOT",
                "output": str(args.output),
                "event": event,
                "invalidated_artifact_count": len(event["invalidated_artifact_ids"]),
                "invalidated_approval_count": event["invalidated_approval_count"],
                "original_input_mutated": False,
            }, ensure_ascii=False, indent=2))
            return 0
        if args.command == "hash":
            print(content_hash(_load_json(args.input)))
            return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
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
