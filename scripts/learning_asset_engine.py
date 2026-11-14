#!/usr/bin/env python3
"""Fail-closed validation for PROMKES learning/asset/drift/outcome governance.

No network fetch, scheduler, baseline mutation, capability approval or release action.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise SystemExit("jsonschema is required; install requirements-dev.txt") from exc

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/"schemas/v4/learning-governance.schema.json"
LANE_RANK={"R0":0,"R1":1,"R2":2,"R3":3,"UNKNOWN":2}
PROCESS_METRICS={"CYCLE_TIME","REVIEWER_EFFORT","REWORK_RATE","FIRST_PASS_ACCEPTANCE","APPROVED_REUSE_RATE","STALE_EVIDENCE_DETECTION_LATENCY","TRACE_COMPLETENESS","RISK_MISCLASSIFICATION","QA_ESCAPE_COUNT"}
class RecordError(ValueError): pass

def _pairs(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise RecordError("duplicate JSON key: "+k)
        out[k]=v
    return out

def load(path):
    try: return json.loads(Path(path).read_text(encoding="utf-8"),object_pairs_hook=_pairs)
    except Exception as e: raise RecordError(f"{path}: {e}") from e

def schema_errors(kind,row):
    schema=load(SCHEMA)
    if kind not in schema["$defs"]: return ["unknown record kind: "+kind]
    return [f"{list(e.path)}: {e.message}" for e in Draft202012Validator(schema["$defs"][kind]).iter_errors(row)]

def validate_formula(x):
    errors=schema_errors("formula",x)
    if errors:return errors
    if x["lifecycle_status"]=="APPROVED":
        if x["rights_status"]!="CLEAR":errors.append("APPROVED requires rights_status=CLEAR")
        if not any(r["status"]=="PASS" and r.get("evidence_ref") for r in x["validation_runs"]):errors.append("APPROVED requires PASS test with evidence")
        qa=x["s12_qa"]
        if qa["status"]!="PASS" or not qa.get("reviewer_ref") or not qa.get("evidence_ref"):errors.append("APPROVED requires independent S12 PASS and evidence")
        a=x.get("human_approval")
        if not a:errors.append("APPROVED requires human_approval")
        elif a["approved_content_sha256"]!=x["content_sha256"]:errors.append("approval must bind the exact formula content hash")
        if x["model_binding"]["binding_type"]=="EXACT_VERSION" and x["model_binding"]["model_version"] in {"UNKNOWN","LATEST"}:errors.append("exact model binding requires a concrete version")
    elif x.get("human_approval") is not None:errors.append("human approval cannot be attached before APPROVED")
    return errors

def reusable_formulas(records,request):
    out=[]
    for x in records:
        if validate_formula(x):continue
        s=x["scope"];b=x["model_binding"]
        if x["lifecycle_status"]!="APPROVED" or x["rights_status"]!="CLEAR":continue
        if request.get("task_type") not in s["task_types"] or request.get("audience_context") not in s["audience_contexts"] or request.get("language") not in s["allowed_languages"]:continue
        if b["binding_type"]=="EXACT_VERSION" and (request.get("provider"),request.get("model"),request.get("model_version"))!=(b["provider"],b["model"],b["model_version"]):continue
        out.append(x)
    return out

def validate_observation(x):
    e=schema_errors("observation",x)
    if e:return e
    if x["fetch_status"]=="SUCCESS":
        if not x.get("normalized_sha256"):e.append("SUCCESS requires normalized hash")
        if x.get("error_code"):e.append("SUCCESS cannot carry an error code")
    else:
        if x.get("normalized_sha256") is not None:e.append("failed fetch/parse cannot claim normalized hash")
        if not x.get("error_code"):e.append("failed fetch/parse requires error code")
    return e

def compare_drift(observation,baseline):
    e=validate_observation(observation)+schema_errors("baseline",baseline)
    if e:raise RecordError("; ".join(e))
    if observation["fetch_status"]!="SUCCESS":return "SOURCE_UNAVAILABLE"
    if observation["normalizer_version"]!=baseline["normalizer_version"]:return "NORMALIZER_MISMATCH_REVIEW"
    if observation["endpoint_id"]!=baseline["endpoint_id"]:return "ENDPOINT_IDENTITY_MISMATCH_REVIEW"
    if observation["normalized_sha256"]!=baseline["normalized_sha256"]:return "REVIEW_REQUIRED"
    return "NO_CHANGE_OBSERVED"

def validate_advice(x):
    e=schema_errors("advice",x)
    if e:return e
    sel=x["selected_candidate_id"];actor=x["selection_actor"]
    if sel is None and actor is not None:e.append("selection actor requires explicit candidate selection")
    if sel is not None and sel not in {c["candidate_id"] for c in x["candidates"]}:e.append("selected candidate is not in candidate list")
    if sel is not None and actor not in {"USER","PROJECT_OWNER"}:e.append("selection must be explicitly attributed to USER or PROJECT_OWNER")
    return e

def validate_outcome(x):
    e=schema_errors("outcome",x)
    if e:return e
    if x["metric"] not in PROCESS_METRICS:e.append("metric outside process-only allowlist")
    if x["denominator"]==0 and x["value"] is not None:e.append("value must be null when denominator is zero")
    if x["denominator"]>0 and x["value"] is None:e.append("value is required when denominator is positive")
    if x["numerator"]>x["denominator"] and x["metric"] not in {"CYCLE_TIME","REVIEWER_EFFORT","STALE_EVIDENCE_DETECTION_LATENCY","QA_ESCAPE_COUNT"}:e.append("rate numerator cannot exceed denominator")
    if x["window_end"]<x["window_start"]:e.append("window_end precedes window_start")
    return e

def preflight_plan(x):
    e=schema_errors("preflight",x)
    if e:raise RecordError("; ".join(e))
    lane="R3" if x["critical_trigger"] else ("R2" if x["material_unknown"] or x["declared_risk_lane"]=="UNKNOWN" else x["declared_risk_lane"])
    if LANE_RANK[x["declared_risk_lane"]]>LANE_RANK[lane]:lane=x["declared_risk_lane"]
    if x["s14_status"]!="COMPLETE":return {"status":"BLOCKED","effective_lane":lane,"route_depth":"BLOCKED","s14_mandatory":True,"fast_track":False}
    if lane=="R3":return {"status":"HOLD","effective_lane":"R3","route_depth":"STOP_AND_ESCALATE","s14_mandatory":True,"fast_track":False}
    if lane=="R0" and x.get("s02_disposition")!="NO_MATERIAL_HEALTH_CLAIM":return {"status":"BLOCKED","effective_lane":"R0","route_depth":"BLOCKED","s14_mandatory":True,"fast_track":False}
    return {"status":"READY_FOR_REVIEW","effective_lane":lane,"route_depth":{"R0":"COMPACT","R1":"STANDARD","R2":"FULL"}[lane],"s14_mandatory":True,"fast_track":False}

def validate_bundle(b):
    errors=[f"{list(e.path)}: {e.message}" for e in Draft202012Validator(load(SCHEMA)).iter_errors(b)]
    if errors:return errors
    checks=[("formula","approved_formulas",validate_formula),("observation","drift_observations",validate_observation),("baseline","accepted_model_baselines",lambda x:schema_errors("baseline",x)),("advice","selection_advice",validate_advice),("outcome","outcome_records",validate_outcome),("preflight","preflight_records",lambda x:schema_errors("preflight",x))]
    for kind,key,fn in checks:
        for row in b[key]:errors.extend(f"{kind}: {m}" for m in fn(row))
    return errors

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest="cmd",required=True);s.add_parser("schema-check");v=s.add_parser("validate");v.add_argument("path",type=Path);a=p.parse_args(argv)
    try:
        schema=load(SCHEMA);Draft202012Validator.check_schema(schema)
        if a.cmd=="schema-check":print("PASS: schema valid; no operational capability or approval implied");return 0
        errors=validate_bundle(load(a.path))
        print(json.dumps({"status":"FAIL","errors":errors},indent=2) if errors else '{"status":"PASS","scope":"supplied records only"}')
        return 1 if errors else 0
    except Exception as e:print("BLOCKED: "+str(e),file=sys.stderr);return 2
if __name__=="__main__":raise SystemExit(main())
