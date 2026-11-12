from __future__ import annotations
import copy, json, sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import v4_gate_engine as engine

def project_copy(tmp_path):
    import shutil
    src=ROOT/"examples/v4"; dst=tmp_path/"project"; shutil.copytree(src,dst)
    return engine.strict_json_load(dst/"smoke-project.json"),dst/"smoke-project.json"

def test_all_v4_schemas_are_well_formed():
    from jsonschema import Draft202012Validator
    for path in sorted((ROOT/"schemas/v4").glob("*.schema.json")): Draft202012Validator.check_schema(engine.strict_json_load(path))

def test_smoke_project_passes_schema_and_semantic_validation(tmp_path):
    project,path=project_copy(tmp_path); errors=engine.schema_validate(project,ROOT/"schemas/v4/project.schema.json")
    for bucket,name in (("claims","claim-record.schema.json"),("scenes","scene-record.schema.json"),("artifacts","artifact-envelope.schema.json"),("capabilities","capability-record.schema.json")):
        for row in project[bucket]: errors+=engine.schema_validate(row,ROOT/"schemas/v4"/name)
    errors+=engine.semantic_validate(project,path); assert errors==[]

def test_canonical_json_hash_is_stable_across_key_order_and_unicode_form():
    assert engine.sha256_json({"b":"café","a":1})==engine.sha256_json({"a":1,"b":"cafe\u0301"})

def test_duplicate_json_keys_are_rejected(tmp_path):
    p=tmp_path/"duplicate.json"; p.write_text('{"safe": true, "safe": false}',encoding="utf-8")
    with pytest.raises(engine.EngineError,match="Duplicate JSON key"): engine.strict_json_load(p)

def test_dependency_invalidation_propagates_transitively(tmp_path):
    project,path=project_copy(tmp_path); assert engine.compute_invalidations(project,"SRC-001")==["ART-001","CLM-001","SCN-001"]

def test_dependency_cycles_are_rejected(tmp_path):
    project,path=project_copy(tmp_path); project["dependencies"].append({"from_id":"ART-001","to_id":"SRC-001"})
    _,errors=engine.dependency_graph(project); assert any(e["code"]=="DEPENDENCY_CYCLE" for e in errors)

def test_path_traversal_and_absolute_paths_are_rejected():
    for value in ("../secret","/etc/passwd","a/../../b","./hidden","a\\b","a//b"): assert not engine.safe_relative_path(value),value
    assert engine.safe_relative_path("assets/logo.png")

def test_project_claim_referencing_missing_source_fails(tmp_path):
    project,path=project_copy(tmp_path); project["claims"][0]["source_ids"]=["SRC-MISSING"]
    assert any(e["code"]=="CLAIM_SOURCE_MISSING" for e in engine.semantic_validate(project,path))

def test_unverified_claim_cannot_authorize_wording(tmp_path):
    project,path=project_copy(tmp_path); project["claims"][0]["status"]="UNVERIFIED"; project["claims"][0]["allowed_wording"]=["Say this anyway"]
    assert any(e["code"]=="CLAIM_WORDING_FAIL_CLOSED" for e in engine.semantic_validate(project,path))

def test_health_claim_without_clinician_review_fails(tmp_path):
    project,path=project_copy(tmp_path); project["claims"][0]["reviewer_role"]="LEGAL"
    assert any(e["code"]=="CLINICAL_REVIEW_MISSING" for e in engine.semantic_validate(project,path))

def test_scene_gap_or_overlap_fails(tmp_path):
    project,path=project_copy(tmp_path); second=copy.deepcopy(project["scenes"][0]); second.update(scene_id="SCN-002",order=1,start_frame=70,end_frame=100); project["scenes"].append(second)
    assert any(e["code"]=="SCENE_TIMELINE_GAP_OR_OVERLAP" for e in engine.semantic_validate(project,path))

def test_scene_duplicate_ids_fail(tmp_path):
    project,path=project_copy(tmp_path); project["scenes"].append(copy.deepcopy(project["scenes"][0])); _,errors=engine.index_records(project["scenes"],"scene_id")
    assert any(e["code"]=="ID_DUPLICATE" for e in errors)

def test_asset_symlink_or_traversal_fails(tmp_path):
    project,path=project_copy(tmp_path); project["assets"]=[{"asset_id":"A","path":"../outside.png","required":False}]
    assert any(e["code"]=="ASSET_PATH_UNSAFE" for e in engine.semantic_validate(project,path))

def test_artifact_hash_mismatch_fails(tmp_path):
    project,path=project_copy(tmp_path); project["artifacts"][0]["content_hash"]="sha256:"+"0"*64
    assert any(e["code"]=="ARTIFACT_HASH_MISMATCH" for e in engine.semantic_validate(project,path))

def test_capability_expiry_fails_closed(tmp_path):
    project,path=project_copy(tmp_path); project["capabilities"][0]["expires_at"]="2020-01-01T00:00:00Z"
    assert any(e["code"]=="CAPABILITY_EXPIRED_OR_UNDATED" for e in engine.semantic_validate(project,path))

def test_renderer_target_version_mismatch_blocks(tmp_path):
    project,path=project_copy(tmp_path); project["renderer_target"]["exact_version"]="1.0.0-not-the-verified-version"
    ok,_=engine.control_check(project,path,"renderer_fail_closed"); assert not ok

def test_rights_pending_blocks(tmp_path):
    project,path=project_copy(tmp_path); project["policy"]["rights_status"]="PENDING"; ok,_=engine.control_check(project,path,"rights_clearance"); assert not ok

def test_unknown_privacy_blocks(tmp_path):
    project,path=project_copy(tmp_path); project["policy"]["privacy_classification"]="UNKNOWN"; ok,_=engine.control_check(project,path,"privacy_classification"); assert not ok

def test_prompt_injection_boundary_failure_blocks(tmp_path):
    project,path=project_copy(tmp_path); project["prompt_preflight"]["source_instructions_executed"]=True
    ok,_=engine.control_check(project,path,"prompt_firewall"); assert not ok

def test_resource_ceiling_exceeded_fails(tmp_path):
    project,path=project_copy(tmp_path); project["budget"]["actual_cost"]=11; ok,_=engine.control_check(project,path,"resource_ceiling"); assert not ok

def test_ed25519_approval_signature_rejects_payload_tampering(tmp_path):
    project,path=project_copy(tmp_path); approval=project["approvals"][0]
    assert engine.verify_approval_signature(approval,project["trusted_signing_keys"])[0]
    approval["scope"]="changed after signing"; ok,reason=engine.verify_approval_signature(approval,project["trusted_signing_keys"])
    assert not ok and "verification failed" in reason

def test_approval_must_be_trusted_and_hash_bound(tmp_path):
    project,path=project_copy(tmp_path); project["approvals"][0]["artifact_hashes"]=["sha256:"+"b"*64]
    errors=engine.semantic_validate(project,path); assert any(e["code"]=="APPROVAL_NOT_HASH_BOUND" for e in errors)

def test_gate_transition_fails_closed_without_control_evidence(tmp_path):
    project,path=project_copy(tmp_path); report=engine.evaluate_gates(project,path,"G7_RELEASE_APPROVED")
    assert report["overall"]=="BLOCKED" and report["gates"][0]["status"]=="BLOCKED"
    assert all(g["status"]=="BLOCKED" for g in report["gates"])

def test_gate_fail_closed_control_detects_a_broken_gate_implementation(tmp_path,monkeypatch):
    project,path=project_copy(tmp_path)
    monkeypatch.setattr(engine,"evaluate_gates",lambda *args,**kwargs:{"overall":"PASS","gates":[{"status":"PASS"}]})
    passed,observed=engine.control_check(project,path,"gate_fail_closed")
    assert not passed and "incorrectly passed" in observed

def test_control_evidence_becomes_stale_when_project_inputs_change(tmp_path):
    project,path=project_copy(tmp_path); report=engine.run_controls(project,path); project["control_results"]=report["results"]
    project["policy"]["privacy_classification"]="INTERNAL"; ok,observed=engine.control_check(project,path,"control_evidence_integrity")
    assert not ok and "invalid evidence" in observed
    assert engine.evaluate_gates(project,path,"G6_CODE_VALID")["overall"]=="BLOCKED"

def test_control_evidence_hash_tampering_is_detected(tmp_path):
    project,path=project_copy(tmp_path); results=engine.run_controls(project,path); results["results"][0]["evidence_hash"]="sha256:"+"0"*64
    project["control_results"]=results["results"]; ok,_=engine.control_check(project,path,"control_evidence_integrity"); assert not ok

def test_visual_lock_requires_reviewer_time_and_hash(tmp_path):
    project,path=project_copy(tmp_path); project["visual"]["canonical_reference_hash"]="not-a-hash"
    ok,_=engine.control_check(project,path,"visual_reference_lock"); assert not ok

def test_all_implemented_controls_are_executed_and_pass_on_smoke_fixture(tmp_path):
    project,path=project_copy(tmp_path); report=engine.run_controls(project,path)
    assert report["executed_control_count"]==len(engine.CONTROL_REGISTRY)==21
    assert report["overall"]=="PASS" and report["counts"]=={"PASS":21,"FAIL":0}
    assert all(engine.valid_control_evidence(row) for row in report["results"])

def test_each_control_has_a_negative_test_or_explicit_fail_closed_test(tmp_path):
    project,path=project_copy(tmp_path)
    mutants={
    "claim_source_integrity":lambda p:p["claims"][0].update(source_ids=["NOPE"]),
    "claim_fail_closed":lambda p:(p["claims"][0].update(status="UNVERIFIED"),p["claims"][0].update(allowed_wording=["unsafe"])),
    "clinical_review":lambda p:p["claims"][0].update(reviewer_role="LEGAL"),
    "source_provenance":lambda p:p["sources"][0].update(verification_status="UNVERIFIED"),
    "scene_timing":lambda p:p["scenes"][0].update(end_frame=0),
    "scene_identity":lambda p:p["scenes"].append(copy.deepcopy(p["scenes"][0])),
    "dependency_integrity":lambda p:p["dependencies"].append({"from_id":"ART-001","to_id":"SRC-001"}),
    "asset_path_safety":lambda p:p["assets"].append({"asset_id":"A","path":"../escape","required":False}),
    "artifact_hash_integrity":lambda p:p["artifacts"][0].update(content_hash="sha256:"+"0"*64),
    "capability_evidence":lambda p:p["capabilities"][0].update(expires_at="2020-01-01T00:00:00Z"),
    "renderer_fail_closed":lambda p:p["renderer_target"].update(exact_version="mismatch"),
    "rights_clearance":lambda p:p["policy"].update(rights_status="PENDING"),
    "privacy_classification":lambda p:p["policy"].update(privacy_classification="UNKNOWN"),
    "prompt_firewall":lambda p:p["prompt_preflight"].update(source_instructions_executed=True),
    "resource_ceiling":lambda p:p["budget"].update(actual_cost=999),
    "approval_hash_binding":lambda p:p["approvals"][0].update(artifact_hashes=["sha256:"+"0"*64]),
    "invalidation_propagation":lambda p:p["invalidation_test"].update(expected_invalidated=[]),
    "artifact_status_integrity":lambda p:p["artifacts"][0].update(validation_result="FAIL"),
    "control_evidence_integrity":lambda p:p.update(control_results=[{"control_id":"X","test_id":"T","oracle":"test","observed":"tampered","status":"PASS","executed_at":"2026-11-12T00:00:00Z","environment":{"ci":True},"engine_version":engine.ENGINE_VERSION,"evidence_hash":"sha256:"+"0"*64}]),
    "visual_reference_lock":lambda p:p["visual"].update(canonical_reference_hash="broken")}
    assert set(mutants)=={adapter for _,adapter,_ in engine.CONTROL_REGISTRY}-{"gate_fail_closed"}
    for _,adapter,_ in engine.CONTROL_REGISTRY:
        if adapter=="gate_fail_closed": continue
        mutant=copy.deepcopy(project); mutants[adapter](mutant); passed,observed=engine.control_check(mutant,path,adapter)
        assert not passed,f"{adapter} unexpectedly passed after negative mutation: {observed}"

def test_gate_engine_passes_pre_release_gates_but_blocks_synthetic_release(tmp_path):
    project,path=project_copy(tmp_path); report=engine.run_controls(project,path); project["control_results"]=report["results"]
    pre=engine.evaluate_gates(project,path,"G6_CODE_VALID")
    assert pre["overall"]=="PASS" and [g["status"] for g in pre["gates"]]==["PASS"]*7
    release=engine.evaluate_gates(project,path,"G7_RELEASE_APPROVED")
    assert release["overall"]=="BLOCKED" and release["gates"][-1]["status"]=="BLOCKED"
    assert any("TEST_FIXTURE" in reason for reason in release["gates"][-1]["reasons"])

def test_cli_validate_run_controls_and_gate_are_reproducible(tmp_path):
    project,path=project_copy(tmp_path)
    import subprocess
    validate=subprocess.run([sys.executable,str(ROOT/"scripts/v4_gate_engine.py"),"validate",str(path),"--schema-dir",str(ROOT/"schemas/v4")],capture_output=True,text=True)
    assert validate.returncode==0,validate.stdout+validate.stderr
    report_path=tmp_path/"controls.json"; updated_path=tmp_path/"updated-project.json"
    controls=subprocess.run([sys.executable,str(ROOT/"scripts/v4_gate_engine.py"),"run-controls",str(path),"--report",str(report_path),"--updated-project",str(updated_path)],capture_output=True,text=True)
    assert controls.returncode==0,controls.stdout+controls.stderr
    updated=engine.strict_json_load(updated_path)
    assert engine.evaluate_gates(updated,updated_path,"G6_CODE_VALID")["overall"]=="PASS"
    assert engine.evaluate_gates(updated,updated_path,"G7_RELEASE_APPROVED")["overall"]=="BLOCKED"

def test_candidate_generator_is_not_misrepresented_as_execution():
    registry=engine.strict_json_load(ROOT/"schemas/v4/control-registry.v4.json")
    assert registry["control_count"]==len(engine.CONTROL_REGISTRY) and registry["status"]=="IMPLEMENTED_EXECUTABLE_CORE"

def test_active_control_registry_matches_engine_adapters_and_gate_map():
    registry=engine.strict_json_load(ROOT/"schemas/v4/control-registry.v4.json")
    expected={r["control_id"]:r["adapter"] for r in registry["controls"]}
    actual={cid:adapter for cid,adapter,_ in engine.CONTROL_REGISTRY}
    assert expected==actual and set().union(*engine.GATE_CONTROLS.values())==set(actual)
