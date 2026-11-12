import pytest
from scripts.v4_control_risk_triage import triage


def sample_registry():
    import itertools
    domains=["EVIDENCE","SOURCE_INTEGRITY","NARRATIVE","VISUAL","MOTION","PROMPT","AUDIO","RENDERER_CODE","SECURITY_PRIVACY_RIGHTS","QA_RELEASE"]
    gates=["INTAKE","FACT_LOCK","NARRATIVE_LOCK","VISUAL_LOCK","PROMPT_PREFLIGHT","MOTION_LOCK","MANIFEST_LOCK","CODE_LOCK","RENDER_GATE","RELEASE_GATE"]
    families=["SCHEMA","PROVENANCE","RED_TEAM_INJECTION","CONSISTENCY_REGRESSION","TIMING_ARITHMETIC","CAPABILITY_COMPATIBILITY","ACCESSIBILITY","RIGHTS_PRIVACY","ARTIFACT_INSPECTION","HUMAN_SIGNOFF"]
    return {"registry_version":"0.1.0","controls":[
      {"control_id":f"CTL-{d}-{g}-{f}","domain":d,"gate":g,"test_family":f,
       "execution_status":"NOT_RUN","verdict":"NOT_VERIFIED"}
      for d,g,f in itertools.product(domains,gates,families)
    ]}


def test_triage_covers_all_candidates_without_claiming_execution():
    report=triage(sample_registry())
    assert report["candidate_count"]==1000
    assert sum(report["summary"]["priority_counts"].values())==1000
    assert sum(report["summary"]["applicability_candidate_counts"].values())==1000
    assert report["summary"]["executed_count"]==0
    assert report["summary"]["not_run_count"]==1000
    assert report["summary"]["not_verified_count"]==1000
    assert all(x["applicability_state"]=="NEEDS_PROJECT_REVIEW" for x in report["controls"])
    assert all(x["triage_disposition"]=="REVIEW_BEFORE_EXECUTION" for x in report["controls"])


def test_security_candidates_rank_above_low_risk_timing():
    report=triage({"controls":[
      {"control_id":"LOW","domain":"NARRATIVE","gate":"NARRATIVE_LOCK","test_family":"TIMING_ARITHMETIC"},
      {"control_id":"HIGH","domain":"SECURITY_PRIVACY_RIGHTS","gate":"PROMPT_PREFLIGHT","test_family":"RED_TEAM_INJECTION"}
    ]})
    assert report["controls"][0]["control_id"]=="HIGH"
    assert report["controls"][0]["risk"]["priority"] in {"P0","P1"}


def test_unknown_taxonomy_fails_closed():
    with pytest.raises(KeyError):
        triage({"controls":[{"control_id":"X","domain":"UNKNOWN","gate":"UNKNOWN","test_family":"UNKNOWN"}]})


def test_duplicate_candidate_ids_fail_closed():
    row={"control_id":"DUP","domain":"EVIDENCE","gate":"FACT_LOCK","test_family":"SCHEMA"}
    with pytest.raises(ValueError,match="unique control_id"):
        triage({"controls":[row,row]})
