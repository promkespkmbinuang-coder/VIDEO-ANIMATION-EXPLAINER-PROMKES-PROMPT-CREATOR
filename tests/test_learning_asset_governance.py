from __future__ import annotations
import copy, sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"scripts"))
import learning_asset_engine as e
H="sha256:"+"a"*64;T="2026-11-14T00:00:00Z"
def formula():
 return {"formula_id":"AFL-F-1","title":"Neutral visual formula","formula_version":"1.0","lifecycle_status":"APPROVED","formula_body":"A neutral prompt formula","content_sha256":H,"provenance":[{"source_id":"SRC-1","locator":"docs/source.md","source_type":"INTERNAL_ARTIFACT","observed_at":T}],"rights_status":"CLEAR","scope":{"task_types":["visual"],"audience_contexts":["general"],"allowed_languages":["id"],"exclusions":["clinical interpretation"]},"model_binding":{"provider":"p","model":"m","model_version":"1.2","binding_type":"EXACT_VERSION"},"validation_runs":[{"test_id":"T1","status":"PASS","tested_at":T,"evidence_ref":"test://1"}],"s12_qa":{"status":"PASS","reviewer_ref":"S12","reviewed_at":T,"evidence_ref":"qa://1"},"claim_refs":[],"human_approval":{"approver_ref":"owner","authority_basis":"rights holder","approved_at":T,"approved_content_sha256":H,"decision":"APPROVE"}}
def observation(status="SUCCESS",digest=H):
 return {"observation_id":"MDS-1","provider":"p","model":"m","endpoint_id":"DOC-1","endpoint_url":"https://example.org/docs","observed_at":T,"fetch_status":status,"normalizer_version":"n1","normalized_sha256":digest if status=="SUCCESS" else None,"snapshot_ref":"snap://1" if status=="SUCCESS" else None,"error_code":None if status=="SUCCESS" else "HTTP_503","http_status":200 if status=="SUCCESS" else 503}
def baseline():
 return {"baseline_id":"BASE-1","provider":"p","model":"m","endpoint_id":"DOC-1","endpoint_url":"https://example.org/docs","model_version":"1.2","normalized_sha256":H,"normalizer_version":"n1","accepted_at":T,"reviewer_ref":"human","evidence_ref":"review://1","decision":"HUMAN_ACCEPTED"}
def preflight(lane="R1",**kw):
 x={"preflight_id":"RPF-1","declared_risk_lane":lane,"material_unknown":False,"critical_trigger":False,"s14_status":"COMPLETE","s02_disposition":"FACT_LOCKED","route_depth":"STANDARD","fast_track":False};x.update(kw);return x
def test_schema_valid():e.Draft202012Validator.check_schema(e.load(e.SCHEMA))
def test_formula_approval_requires_rights_tests_s12_and_hash_bound_approval():
 x=formula();assert e.validate_formula(x)==[]
 x["rights_status"]="UNKNOWN";assert e.validate_formula(x)
 x=formula();x["human_approval"]["approved_content_sha256"]="sha256:"+"b"*64;assert any("exact formula" in m for m in e.validate_formula(x))
def test_reuse_filters_unapproved_and_exact_model_version():
 approved=formula();draft=copy.deepcopy(approved);draft["formula_id"]="AFL-F-2";draft["lifecycle_status"]="CANDIDATE";draft["human_approval"]=None
 req={"task_type":"visual","audience_context":"general","language":"id","provider":"p","model":"m","model_version":"1.2"}
 assert len(e.reusable_formulas([approved,draft],req))==1
 req["model_version"]="2.0";assert e.reusable_formulas([approved],req)==[]
def test_failed_drift_fetch_is_not_no_change():assert e.compare_drift(observation("FETCH_ERROR"),baseline())=="SOURCE_UNAVAILABLE"
def test_hash_change_requires_review_and_does_not_mutate_baseline():
 b=baseline();x=observation(digest="sha256:"+"b"*64);assert e.compare_drift(x,b)=="REVIEW_REQUIRED";assert b==baseline()
def test_normalizer_change_requires_review():
 x=observation();x["normalizer_version"]="n2";assert e.compare_drift(x,baseline())=="NORMALIZER_MISMATCH_REVIEW"
def test_s14_mandatory_in_all_lanes():
 r=e.preflight_plan(preflight("R0",s14_status="NOT_RUN",s02_disposition="NO_MATERIAL_HEALTH_CLAIM"));assert r["status"]=="BLOCKED" and r["s14_mandatory"]
def test_unknown_goes_r2_and_critical_wins():
 assert e.preflight_plan(preflight("UNKNOWN",material_unknown=True))["effective_lane"]=="R2"
 r=e.preflight_plan(preflight("R1",critical_trigger=True));assert r["effective_lane"]=="R3" and r["route_depth"]=="STOP_AND_ESCALATE"
def test_r0_requires_s02_disposition():
 assert e.preflight_plan(preflight("R0"))["status"]=="BLOCKED"
 assert e.preflight_plan(preflight("R0",s02_disposition="NO_MATERIAL_HEALTH_CLAIM"))["route_depth"]=="COMPACT"
def test_fast_track_is_never_enabled():assert e.preflight_plan(preflight())["fast_track"] is False
def test_advisor_non_authoritative_and_max_three():
 x={"advice_id":"MSA-1","created_at":T,"task_type":"video","advisory_only":True,"candidates":[{"candidate_id":"A","provider":"p","model":"m","model_version":"1","feature_evidence":[{"feature":"i2v","status":"UNKNOWN","evidence_ref":None}],"tradeoff":"unknown"}],"tradeoffs":[],"unknowns":[],"selected_candidate_id":None,"selection_actor":None}
 assert e.validate_advice(x)==[]
 x["candidates"]*=4;assert e.validate_advice(x)
def test_selection_requires_explicit_human_actor():
 x={"advice_id":"MSA-1","created_at":T,"task_type":"video","advisory_only":True,"candidates":[{"candidate_id":"A","provider":"p","model":"m","model_version":"1","feature_evidence":[],"tradeoff":"unknown"}],"tradeoffs":[],"unknowns":[],"selected_candidate_id":"A","selection_actor":None}
 assert e.validate_advice(x)
def test_outcomes_are_process_only_and_have_denominator():
 x={"outcome_id":"POR-1","metric":"REWORK_RATE","data_scope":"PROCESS_ONLY","cohort_ref":"w46","window_start":"2026-11-01T00:00:00Z","window_end":"2026-11-08T00:00:00Z","numerator":2,"denominator":10,"value":0.2,"unit":"ratio","missing_count":0,"evidence_ref":"report://1","limitations":["descriptive"]}
 assert e.validate_outcome(x)==[]
 x["data_scope"]="AUDIENCE_HEALTH_BEHAVIOR";assert e.validate_outcome(x)
def test_duplicate_keys_fail_closed(tmp_path):
 p=tmp_path/"dup.json";p.write_text('{"x":1,"x":2}',encoding="utf-8")
 with pytest.raises(e.RecordError,match="duplicate JSON key"):e.load(p)
