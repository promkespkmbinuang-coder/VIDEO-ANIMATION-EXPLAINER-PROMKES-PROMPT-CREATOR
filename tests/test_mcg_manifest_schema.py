import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/v4/mcg-manifest.schema.json"
EXAMPLE = ROOT / "docs/mcg/mcg-manifest.example.json"

OWNERS = {
 "GUIDE-01":"S05:visual-identity-art-direction",
 "GUIDE-02":"S04:story-screenplay-architect",
 "GUIDE-03":"S05:visual-identity-art-direction",
 "GUIDE-04":"S04:story-screenplay-architect",
 "GUIDE-05":"S09:voice-sound-design",
 "GUIDE-06":"S05:visual-identity-art-direction",
 "GUIDE-07":"S13:continuity-guardian"
}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_mcg_schema_is_valid_and_example_is_draft_valid():
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    m = load(EXAMPLE)
    assert list(Draft202012Validator(schema).iter_errors(m)) == []
    assert m["status"] == "DRAFT"

def test_exact_seven_single_owner_guides():
    m = load(EXAMPLE)
    assert len(m["guide_registry"]) == 7
    assert {g["guide_id"]:g["primary_owner"] for g in m["guide_registry"]} == OWNERS

def test_exact_three_protocols():
    m = load(EXAMPLE)
    assert {p["protocol_id"] for p in m["protocol_refs"]} == {"GCL-01","CCM-01","CQA-01"}
    assert len(m["protocol_refs"]) == 3

def test_health_truth_is_s02_owned_and_does_not_embed_claim_text():
    m = load(EXAMPLE)
    assert m["health_truth_registry_ref"]["owner"] == "S02:health-evidence-safety-auditor"
    for claim in m["health_truth_registry_ref"]["claim_refs"]:
        assert "claim" not in claim
        if claim["status"] == "VERIFIED":
            assert claim["evidence_refs"]

def test_post_storyboard_gate_starts_not_run_and_cannot_claim_ready():
    m = load(EXAMPLE)
    assert m["scene_continuity"]["refresh_gate_status"] == "NOT_RUN"
    m["status"] = "READY_FOR_SCENE_PROMPTS"
    assert list(Draft202012Validator(load(SCHEMA)).iter_errors(m))
