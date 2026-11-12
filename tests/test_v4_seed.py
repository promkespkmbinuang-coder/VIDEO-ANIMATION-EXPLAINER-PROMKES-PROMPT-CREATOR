import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_v4_schemas_are_valid_json_schema():
    for rel in (
        "schemas/v4/claim-record.schema.json",
        "schemas/v4/artifact-envelope.schema.json",
    ):
        Draft202012Validator.check_schema(load_json(rel))


def test_claim_schema_fails_closed_for_unverified_claims():
    schema = load_json("schemas/v4/claim-record.schema.json")
    validator = Draft202012Validator(schema)
    record = {
        "claim_id": "CLM-TEST-01",
        "text": "Example claim",
        "claim_type": "PREVENTION",
        "source_ids": ["SRC-01"],
        "evidence_level": "UNVERIFIED",
        "population": "Adults",
        "jurisdiction": "ID",
        "valid_from": None,
        "valid_to": None,
        "status": "UNVERIFIED",
        "allowed_wording": ["This should not pass"],
        "forbidden_wording": [],
        "reviewed_by_human": False,
        "reviewer_role": "NONE",
        "schema_version": "1.0.0",
    }
    assert list(validator.iter_errors(record))


def test_claim_schema_requires_identity_for_human_review():
    schema = load_json("schemas/v4/claim-record.schema.json")
    record = {
        "claim_id": "CLM-TEST-02",
        "text": "Supported example claim",
        "claim_type": "OTHER",
        "source_ids": ["SRC-02"],
        "evidence_level": "PRIMARY",
        "population": "Adults",
        "jurisdiction": "ID",
        "status": "VERIFIED",
        "allowed_wording": ["Constrained wording"],
        "forbidden_wording": [],
        "reviewed_by_human": True,
        "reviewer_role": "CLINICIAN",
        "schema_version": "1.0.0",
    }
    assert list(Draft202012Validator(schema).iter_errors(record))


def test_control_enumerator_creates_1000_unexecuted_candidates(tmp_path):
    script = ROOT / "scripts/generate_v4_control_candidates.py"
    output = tmp_path / "control-candidates.json"
    run = subprocess.run(
        [sys.executable, str(script), "--output", str(output)],
        check=True,
        capture_output=True,
        text=True,
    )
    registry = json.loads(output.read_text(encoding="utf-8"))
    controls = registry["controls"]
    assert registry["candidate_count"] == 1000
    assert len(controls) == 1000
    assert len({row["control_id"] for row in controls}) == 1000
    assert all(row["execution_status"] == "NOT_RUN" for row in controls)
    assert all(row["verdict"] == "NOT_VERIFIED" for row in controls)
    assert "none were executed" in run.stdout
