import json
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.validate_motion_contract import (
    ADAPTER_SCHEMA,
    MOTION_SCHEMA,
    validate_motion_record,
    validate_platform_adapter,
)

ROOT = Path(__file__).resolve().parents[1]


def load_fixture(name: str):
    return json.loads((ROOT / "tests/fixtures/v4" / name).read_text(encoding="utf-8"))


def test_motion_and_adapter_schemas_are_valid():
    Draft202012Validator.check_schema(json.loads(MOTION_SCHEMA.read_text(encoding="utf-8")))
    Draft202012Validator.check_schema(json.loads(ADAPTER_SCHEMA.read_text(encoding="utf-8")))


def test_draft_motion_and_unchecked_adapter_validate_without_execution_claim():
    assert validate_motion_record(load_fixture("motion-valid.json")) == []
    adapter = load_fixture("platform-adapter-not-checked.json")
    assert validate_platform_adapter(adapter) == []
    assert adapter["status"] == "NOT_CHECKED"


def test_motion_duration_matches_half_open_frame_interval():
    motion = load_fixture("motion-valid.json")
    motion["timing"]["duration_frames"] = 25
    assert any("duration_frames must equal" in error for error in validate_motion_record(motion))


def test_keyframes_and_phases_must_stay_inside_interval():
    motion = load_fixture("motion-valid.json")
    motion["keyframes"][1]["frame"] = 24
    motion["motion_phases"][0]["end_frame_exclusive"] = 25
    errors = validate_motion_record(motion)
    assert any("keyframes[1]" in error for error in errors)
    assert any("motion_phases[0]" in error for error in errors)


def test_s09_audio_timing_preserves_source_precision_and_locator():
    motion = load_fixture("motion-valid.json")
    motion["timing"].update({
        "timing_source": "S09_AUDIO",
        "source_precision": "UNKNOWN",
        "source_time_ref": None,
    })
    errors = validate_motion_record(motion)
    assert any("preserve actual source precision" in error for error in errors)
    assert any("requires source_time_ref" in error for error in errors)


def test_camera_reference_keeps_s06_camera_ownership():
    motion = load_fixture("motion-valid.json")
    motion["target_kind"] = "CAMERA_REFERENCE"
    motion["camera_plan_ref"] = None
    assert any("S06-owned camera plan" in error for error in validate_motion_record(motion))


def test_runtime_tested_adapter_requires_docs_and_runtime_test_evidence():
    adapter = load_fixture("platform-adapter-not-checked.json")
    adapter["status"] = "RUNTIME_TESTED"
    adapter["checked_at"] = "2026-11-13T00:00:00Z"
    adapter["feature_matrix"][0]["support"] = "SUPPORTED"
    adapter["feature_matrix"][0]["evidence_refs"] = ["EVD-1"]
    errors = validate_platform_adapter(adapter)
    assert any("official_docs_refs" in error for error in errors)
    assert any("runtime_test_refs" in error for error in errors)


def test_non_unknown_feature_claim_requires_evidence():
    adapter = load_fixture("platform-adapter-not-checked.json")
    adapter["feature_matrix"][0]["support"] = "SUPPORTED"
    assert any("requires evidence_refs" in error for error in validate_platform_adapter(adapter))
