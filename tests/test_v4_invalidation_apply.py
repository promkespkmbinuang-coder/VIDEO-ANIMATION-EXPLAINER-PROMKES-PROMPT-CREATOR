from __future__ import annotations

import copy

import pytest

from scripts.v4_gate_engine import apply_invalidation, content_hash, validate_record


def _artifact(artifact_id: str, dependencies: list[str]) -> dict:
    row = {
        "artifact_id": artifact_id,
        "artifact_type": "derived_artifact",
        "project_id": "PRJ-INV-TEST",
        "schema_id": "urn:promkes:v4:artifact-envelope",
        "schema_version": "4.0.0",
        "producer_version": "4.0.0",
        "created_at": "2026-11-12T10:00:00Z",
        "updated_at": None,
        "status": "PASS",
        "content_hash": "",
        "validator_id": "promkes-v4-gate-engine",
        "validator_version": "4.0.0",
        "validation_result": "PASS",
        "source_refs": ["SRC-1"],
        "dependency_refs": dependencies,
        "supersedes": None,
        "invalidated_by": None,
        "rights_status": "CLEARED",
        "privacy_classification": "PUBLIC",
        "capability_refs": [],
        "content_path": f"artifacts/{artifact_id}.json",
    }
    row["content_hash"] = content_hash(row)
    return row


def _project() -> dict:
    records = [
        _artifact("SRC-1", []),
        _artifact("CLAIM-1", ["SRC-1"]),
        _artifact("SCRIPT-1", ["CLAIM-1"]),
        _artifact("SCENE-1", ["SCRIPT-1"]),
    ]
    scene_hash = next(x["content_hash"] for x in records if x["artifact_id"] == "SCENE-1")
    return {
        "project_id": "PRJ-INV-TEST",
        "dependency_graph": [
            {"artifact_id": "SRC-1", "depends_on": []},
            {"artifact_id": "CLAIM-1", "depends_on": ["SRC-1"]},
            {"artifact_id": "SCRIPT-1", "depends_on": ["CLAIM-1"]},
            {"artifact_id": "SCENE-1", "depends_on": ["SCRIPT-1"]},
        ],
        "artifact_records": records,
        "approvals": [{
            "domain": "RELEASE",
            "decision": "APPROVED",
            "status": "ACTIVE",
            "artifact_hashes": [scene_hash],
            "approver_id": "producer-1",
        }],
    }


def test_apply_invalidation_marks_transitive_dependents_and_rehashes():
    project = _project()
    revised, event = apply_invalidation(project, ["SRC-1"])
    assert event["invalidated_artifact_ids"] == ["CLAIM-1", "SCENE-1", "SCRIPT-1"]
    revised_map = {x["artifact_id"]: x for x in revised["artifact_records"]}
    assert revised_map["SRC-1"]["status"] == "PASS"
    for artifact_id in ("CLAIM-1", "SCRIPT-1", "SCENE-1"):
        row = revised_map[artifact_id]
        assert row["status"] == "INVALIDATED"
        assert row["validation_result"] == "NOT_RUN"
        assert row["invalidated_by"] == "SRC-1"
        assert validate_record(row, "artifact-envelope") == []
    assert revised["approvals"][0]["status"] == "INVALIDATED"
    assert revised["dependency_graph"][1]["status"] == "INVALIDATED"
    assert revised["last_invalidation_event_id"] == event["event_id"]


def test_apply_invalidation_never_mutates_original_project():
    project = _project()
    original = copy.deepcopy(project)
    revised, _ = apply_invalidation(project, ["SRC-1"])
    assert project == original
    assert revised is not project
    assert revised["artifact_records"][1]["status"] == "INVALIDATED"


def test_apply_invalidation_requires_complete_artifact_envelopes():
    project = _project()
    project["artifact_records"] = [x for x in project["artifact_records"] if x["artifact_id"] != "SCRIPT-1"]
    with pytest.raises(ValueError, match="artifact envelopes are missing"):
        apply_invalidation(project, ["SRC-1"])


def test_apply_invalidation_rejects_dependency_cycles():
    project = _project()
    for node in project["dependency_graph"]:
        if node["artifact_id"] == "SRC-1":
            node["depends_on"] = ["SCENE-1"]
    with pytest.raises(ValueError, match="cycle"):
        apply_invalidation(project, ["SRC-1"])


def test_apply_invalidation_rejects_unknown_changed_artifact():
    with pytest.raises(ValueError, match="Unknown changed artifact"):
        apply_invalidation(_project(), ["UNKNOWN"])
