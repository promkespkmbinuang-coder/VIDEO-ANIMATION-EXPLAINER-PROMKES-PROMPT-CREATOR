from __future__ import annotations

import base64
import json
from datetime import timedelta
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.promkes_v2.trust import TrustRegistry, verify_approval, release_quorum
from scripts.promkes_v2.resource import evaluate_resource_budget
from scripts.promkes_v2.common import canonical_json_bytes
from test_v2_acceptance import NOW, FUTURE, PAST, signed_registry, make_approval

ROOT = Path(__file__).resolve().parents[1]


def test_all_v4_schemas_are_valid_draft_2020_12_and_parseable():
    schema_files = sorted((ROOT / "schemas/v4").glob("*.schema.json"))
    assert len(schema_files) >= 15
    for path in schema_files:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"


def test_control_registry_v2_validates_against_its_dedicated_schema():
    from scripts.promkes_v2.registry import validate_registry
    registry_path = ROOT / "schemas/v4/control-registry.v2.json"
    assert validate_registry(registry_path) == []


def test_all_skill_handoff_envelopes_keep_scope_and_schema_ids():
    schema = json.loads((ROOT / "schemas/v4/handoff-envelope.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["skill_id"]["enum"] == ["M00", *[f"S{i:02d}" for i in range(1, 15)]]
    assert schema["properties"]["lane_id"]["enum"] == ["S10-MP", "S10-RE"]
    assert schema["allOf"]


def test_trust_registry_allows_same_human_multiple_roles_but_quorum_stays_distinct(tmp_path):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    # Recreate a correctly root-signed fixture with one person holding both roles.
    path2, root2, keys2, doc2 = signed_registry(tmp_path / "multi-role")
    person = doc2["authorities"][0]["approver_id"]
    doc2["authorities"][1]["approver_id"] = person
    # The test registry signer is external and deterministic only within this fixture.
    root_private = Ed25519PrivateKey.generate()
    public = root_private.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    doc2["root_fingerprint"] = "sha256:" + __import__("hashlib").sha256(public).hexdigest()
    body2 = {k: v for k, v in doc2.items() if k != "root_signature"}
    doc2["root_signature"] = base64.b64encode(root_private.sign(canonical_json_bytes(body2))).decode()
    path2.write_text(json.dumps(doc2), encoding="utf-8")
    root2 = base64.b64encode(public).decode()
    registry = TrustRegistry.load(path2, pinned_root_public_key_b64=root2, now=NOW)
    h = "sha256:" + "b" * 64
    approvals = [
        make_approval("CLINICIAN", person, "KEY-CLINICAL", keys2["KEY-CLINICAL"], h),
        make_approval("RELEASE_APPROVER", person, "KEY-RELEASE", keys2["KEY-RELEASE"], h),
    ]
    ok, reasons = release_quorum(approvals, registry, required_hashes={h},
                                 required_roles=("CLINICIAN", "RELEASE_APPROVER"),
                                 min_distinct_humans=2, now=NOW)
    assert not ok
    assert any("distinct human quorum" in reason for reason in reasons)


def test_release_quorum_rejects_approval_with_wrong_scope(tmp_path):
    path, root_b64, keys, _ = signed_registry(tmp_path)
    registry = TrustRegistry.load(path, pinned_root_public_key_b64=root_b64, now=NOW)
    h = "sha256:" + "c" * 64
    clinician = make_approval("CLINICIAN", "DR-A", "KEY-CLINICAL", keys["KEY-CLINICAL"], h)
    reviewer = make_approval("RELEASE_APPROVER", "OFFICIAL-B", "KEY-RELEASE", keys["KEY-RELEASE"], h)
    reviewer["scope"] = "CLINICAL_REVIEW"
    reviewer["signature"] = base64.b64encode(keys["KEY-RELEASE"].sign(
        __import__("scripts.promkes_v2.trust", fromlist=["approval_payload"]).approval_payload(reviewer)
    )).decode()
    ok, reasons = release_quorum([clinician, reviewer], registry, required_hashes={h},
                                 required_roles=("CLINICIAN", "RELEASE_APPROVER"), now=NOW)
    assert not ok
    assert any("scope must be RELEASE" in reason for reason in reasons)


def test_future_credential_verification_timestamp_is_rejected(tmp_path):
    future = (NOW + timedelta(days=1)).isoformat().replace("+00:00", "Z")
    path, root_b64, _, _ = signed_registry(
        tmp_path, authority_overrides={"KEY-CLINICAL": {"credential_verified_at": future}}
    )
    import pytest
    from scripts.promkes_v2.trust import TrustError
    with pytest.raises(TrustError, match="future-dated"):
        TrustRegistry.load(path, pinned_root_public_key_b64=root_b64, now=NOW)


def test_approved_resource_profile_passes_only_with_root_signed_exact_profile_hash(tmp_path):
    from scripts.promkes_v2.common import sha256_json
    profile = {"status": "APPROVED", "profile_id": "PROFILE-RENDER-01", "approved_by": "OPS-01",
               "approval_ref": "APPROVAL-OPS-01", "route": "PROGRAMMATIC_RENDER",
               "ceilings": {"provider_cost": 12.0, "render_seconds": 300}}
    trusted = {"PROFILE-RENDER-01": {"route": "PROGRAMMATIC_RENDER", "content_hash": sha256_json(profile),
                                      "required_categories": ["provider_cost", "render_seconds"]}}
    usage = {"provider_cost": 5.5, "render_seconds": 120}
    missing_pin = evaluate_resource_budget("PROGRAMMATIC_RENDER", profile, usage,
                                           {"provider_cost", "render_seconds"})
    valid = evaluate_resource_budget("PROGRAMMATIC_RENDER", profile, usage,
                                     {"provider_cost", "render_seconds"},
                                     trusted_profile_records=trusted)
    modified = dict(profile); modified["ceilings"] = {"provider_cost": 999, "render_seconds": 99999}
    tampered = evaluate_resource_budget("PROGRAMMATIC_RENDER", modified, usage,
                                        {"provider_cost", "render_seconds"},
                                        trusted_profile_records=trusted)
    excessive = evaluate_resource_budget("PROGRAMMATIC_RENDER", profile,
                                         {"provider_cost": 13, "render_seconds": 120},
                                         {"provider_cost", "render_seconds"},
                                         trusted_profile_records=trusted)
    assert missing_pin["status"] == "BLOCKED"
    assert valid["status"] == "PASS"
    assert tampered["status"] == "BLOCKED"
    assert excessive["status"] == "FAIL"


def test_resource_profile_schema_rejects_negative_ceilings_and_unexplained_na():
    schema = json.loads((ROOT / "schemas/v4/resource-profile-v2.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    negative = {"status": "APPROVED", "route": "PROGRAMMATIC_RENDER", "profile_id": "P1",
                "approved_by": "OPS", "approval_ref": "A1", "ceilings": {"render_seconds": -1}}
    not_applicable = {"status": "NOT_APPLICABLE", "route": "BLUEPRINT_ONLY", "profile_id": None,
                      "approved_by": None, "approval_ref": None, "ceilings": {}}
    assert list(validator.iter_errors(negative))
    assert list(validator.iter_errors(not_applicable))


def test_release_quorum_rejects_extra_hash_not_in_external_inventory(tmp_path):
    from scripts.promkes_v2.trust import approval_payload
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    path, root_b64, keys, _ = signed_registry(tmp_path)
    registry = TrustRegistry.load(path, pinned_root_public_key_b64=root_b64, now=NOW)
    required_hash = "sha256:" + "d" * 64
    unknown_hash = "sha256:" + "e" * 64
    clinician = make_approval("CLINICIAN", "DR-A", "KEY-CLINICAL", keys["KEY-CLINICAL"], required_hash)
    release = make_approval("RELEASE_APPROVER", "OFFICIAL-B", "KEY-RELEASE", keys["KEY-RELEASE"], required_hash)
    release["artifact_hashes"].append(unknown_hash)
    release["signature"] = base64.b64encode(keys["KEY-RELEASE"].sign(approval_payload(release))).decode()
    ok, reasons = release_quorum([clinician, release], registry, required_hashes={required_hash},
                                 known_hashes={required_hash},
                                 required_roles=("CLINICIAN", "RELEASE_APPROVER"), now=NOW)
    assert not ok
    assert any("unknown artifact hashes" in reason for reason in reasons)


def test_resource_budget_rejects_nan_infinity_and_boolean_measurements():
    from scripts.promkes_v2.common import sha256_json
    profile = {"status": "APPROVED", "profile_id": "PROFILE-1", "approved_by": "OPS",
               "approval_ref": "APR-1", "route": "PROGRAMMATIC_RENDER", "ceilings": {"render_seconds": 100}}
    trusted = {"PROFILE-1": {"route": "PROGRAMMATIC_RENDER", "content_hash": sha256_json(profile),
                             "required_categories": ["render_seconds"]}}
    for value in (float("nan"), float("inf"), True, -1):
        result = evaluate_resource_budget("PROGRAMMATIC_RENDER", profile, {"render_seconds": value},
                                          {"render_seconds"}, trusted_profile_records=trusted)
        assert result["status"] == "FAIL"
    bad_profile = dict(profile); bad_profile["ceilings"] = {"render_seconds": float("nan")}
    assert evaluate_resource_budget("PROGRAMMATIC_RENDER", bad_profile, {"render_seconds": 2},
                                    {"render_seconds"}, trusted_profile_records=trusted)["status"] == "BLOCKED"


def test_benign_source_scan_never_grants_tool_authority():
    from scripts.promkes_v2.firewall import rescan_at_boundary
    result = rescan_at_boundary("Materi edukasi: lakukan PSN 3M Plus secara berkala.")
    assert result["status"] == "PASS_WITH_ISOLATION"
    assert result["allow_tool_execution"] is False
    assert result["source_instruction_execution_allowed"] is False


def test_claim_number_elsewhere_in_document_does_not_support_claim_number():
    from scripts.promkes_v2.evidence import verify_claim_support
    source = "Gunakan kelambu untuk mengurangi kontak dengan nyamuk.\nPada tahun 2024 tercatat 25 kasus di wilayah lain."
    result = verify_claim_support("Gunakan kelambu untuk mengurangi kontak dengan nyamuk pada 25 kasus.",
                                 source, verbatim_quote="Gunakan kelambu untuk mengurangi kontak dengan nyamuk.")
    assert result.status == "INSUFFICIENT"
    assert "25" in result.number_mismatches


def test_semantic_handoff_requires_artifact_index_even_when_schema_is_valid():
    from scripts.promkes_v2.handoff import validate_handoff
    from test_v2_acceptance import valid_handoff, SCHEMA
    errors = validate_handoff(valid_handoff(), SCHEMA, expected_producer="S03")
    assert any("artifact index is required" in error for error in errors)


def test_semantic_handoff_requires_actual_bytes_for_each_artifact_reference(tmp_path):
    from scripts.promkes_v2.handoff import validate_handoff
    from test_v2_acceptance import valid_handoff, SCHEMA
    index = {
        "ART-IN-1": {"content_hash": "sha256:" + "1" * 64, "owner_skill_id": "S01"},
        "ART-OUT-1": {"content_hash": "sha256:" + "2" * 64, "owner_skill_id": "S03"},
    }
    errors = validate_handoff(valid_handoff(), SCHEMA, expected_producer="S03", artifact_index=index)
    assert any("byte path is required" in error for error in errors)


def test_external_trust_registry_exposes_root_signed_resource_profile_hashes(tmp_path):
    from scripts.promkes_v2.common import sha256_json
    profile = {"status": "APPROVED", "profile_id": "PROFILE-EXT", "approved_by": "OPS",
               "approval_ref": "APR-EXT", "route": "PROGRAMMATIC_RENDER",
               "ceilings": {"render_seconds": 90}}
    row = {"profile_id": "PROFILE-EXT", "route": "PROGRAMMATIC_RENDER", "content_hash": sha256_json(profile),
           "required_categories": ["render_seconds"]}
    path, root_b64, _, _ = signed_registry(tmp_path, resource_profiles=[row])
    registry = TrustRegistry.load(path, pinned_root_public_key_b64=root_b64, now=NOW)
    assert registry.resource_profiles == {"PROFILE-EXT": {"route": "PROGRAMMATIC_RENDER", "content_hash": sha256_json(profile),
                                                         "required_categories": ["render_seconds"]}}


def test_handoff_dependency_links_require_external_statuses(tmp_path):
    from scripts.promkes_v2.handoff import validate_handoff
    from test_v2_acceptance import valid_handoff, SCHEMA, sha256_bytes
    from scripts.promkes_v2.common import sha256_json
    artifact = tmp_path / "artifact.json"; artifact.write_text('{"ok":true}', encoding="utf-8")
    digest = sha256_bytes(artifact.read_bytes())
    h = valid_handoff()
    h["input_refs"][0]["content_hash"] = digest
    h["outputs"][0]["content_hash"] = digest
    h["trace_links"] = [{"from_ref": "ART-OUT-1", "to_ref": "ART-IN-1", "relation": "DEPENDS_ON"}]
    h["payload_hash"] = sha256_json(h, omit=("payload_hash",))
    index = {"ART-IN-1": {"path": artifact, "content_hash": digest, "owner_skill_id": "S01"},
             "ART-OUT-1": {"path": artifact, "content_hash": digest, "owner_skill_id": "S03"}}
    errors = validate_handoff(h, SCHEMA, expected_producer="S03", artifact_index=index)
    assert any("upstream dependency status is missing" in error for error in errors)
    errors2 = validate_handoff(h, SCHEMA, expected_producer="S03", artifact_index=index, dependency_statuses={"ART-IN-1": "INVALIDATED"})
    assert any("INVALIDATED is not eligible for consumption" in error for error in errors2)
    assert not validate_handoff(h, SCHEMA, expected_producer="S03", artifact_index=index, dependency_statuses={"ART-IN-1": "PASS"})


def test_handoff_registry_owner_mismatch_is_rejected(tmp_path):
    from scripts.promkes_v2.handoff import validate_handoff
    from test_v2_acceptance import valid_handoff, SCHEMA, sha256_bytes
    artifact = tmp_path / "artifact.json"; artifact.write_text('{"artifact":true}', encoding="utf-8")
    digest = sha256_bytes(artifact.read_bytes())
    h = valid_handoff()
    for ref in h["input_refs"] + h["outputs"]: ref["content_hash"] = digest
    h["payload_hash"] = __import__("scripts.promkes_v2.common", fromlist=["sha256_json"]).sha256_json(h, omit=("payload_hash",))
    index = {"ART-IN-1": {"path": artifact, "content_hash": digest, "owner_skill_id": "S02"},
             "ART-OUT-1": {"path": artifact, "content_hash": digest, "owner_skill_id": "S03"}}
    errors = validate_handoff(h, SCHEMA, expected_producer="S03", artifact_index=index)
    assert any("envelope owner differs" in error for error in errors)


def test_budget_cli_uses_external_signed_registry_and_not_project_allowlist(tmp_path, capsys):
    from scripts.promkes_v2.cli import main
    from scripts.promkes_v2.common import sha256_json
    profile = {"status": "APPROVED", "profile_id": "PROFILE-CLI", "approved_by": "OPS-01",
               "approval_ref": "APR-CLI", "route": "PROGRAMMATIC_RENDER",
               "ceilings": {"render_seconds": 100}}
    row = {"profile_id": "PROFILE-CLI", "route": "PROGRAMMATIC_RENDER", "content_hash": sha256_json(profile),
           "required_categories": ["render_seconds"]}
    project = tmp_path / "project"; project.mkdir()
    input_path = project / "budget.json"
    input_path.write_text(json.dumps({"route": "PROGRAMMATIC_RENDER", "profile": profile,
                                      "usage": {"render_seconds": 40},
                                      "required_categories": ["render_seconds"],
                                      "trusted_profile_ids": ["ATTACKER-CHOSEN-ID"]}), encoding="utf-8")
    registry_path, root_b64, _, _ = signed_registry(tmp_path / "external", resource_profiles=[row])
    code = main(["check-budget", str(input_path), "--trust-registry", str(registry_path),
                 "--pinned-root-key", root_b64, "--project-root", str(project)])
    result = json.loads(capsys.readouterr().out)
    assert code == 0 and result["status"] == "PASS"
    # An otherwise valid signed registry must still be rejected when placed inside the audited project.
    inside = project / "registry.json"; inside.write_bytes(registry_path.read_bytes())
    code2 = main(["check-budget", str(input_path), "--trust-registry", str(inside),
                  "--pinned-root-key", root_b64, "--project-root", str(project)])
    result2 = json.loads(capsys.readouterr().out)
    assert code2 == 1 and result2["status"] == "BLOCKED"


def test_validate_handoff_cli_pins_external_index_and_expected_producer(tmp_path, capsys):
    from scripts.promkes_v2.cli import main
    from scripts.promkes_v2.common import sha256_bytes, sha256_json
    from test_v2_acceptance import valid_handoff
    project = tmp_path / "project"; project.mkdir()
    input_artifact = project / "input.json"; input_artifact.write_text('{"input":1}', encoding="utf-8")
    output_artifact = project / "output.json"; output_artifact.write_text('{"output":1}', encoding="utf-8")
    h = valid_handoff()
    h["input_refs"][0]["content_hash"] = sha256_bytes(input_artifact.read_bytes())
    h["outputs"][0]["content_hash"] = sha256_bytes(output_artifact.read_bytes())
    h["payload_hash"] = sha256_json(h, omit=("payload_hash",))
    handoff_path = project / "handoff.json"; handoff_path.write_text(json.dumps(h), encoding="utf-8")
    index = {
        "ART-IN-1": {"path": str(input_artifact), "content_hash": sha256_bytes(input_artifact.read_bytes()), "owner_skill_id": "S01"},
        "ART-OUT-1": {"path": str(output_artifact), "content_hash": sha256_bytes(output_artifact.read_bytes()), "owner_skill_id": "S03"},
    }
    index_path = tmp_path / "external-artifact-index.json"
    index_path.write_text(json.dumps(index), encoding="utf-8")
    index_pin = sha256_bytes(index_path.read_bytes())
    code = main(["validate-handoff", str(handoff_path), "--artifact-index", str(index_path),
                 "--artifact-index-sha256", index_pin, "--project-root", str(project),
                 "--expected-producer", "S03"])
    result = json.loads(capsys.readouterr().out)
    assert code == 0 and result["status"] == "PASS"

    code2 = main(["validate-handoff", str(handoff_path), "--artifact-index", str(index_path),
                  "--artifact-index-sha256", index_pin, "--project-root", str(project),
                  "--expected-producer", "S04"])
    result2 = json.loads(capsys.readouterr().out)
    assert code2 == 1 and any("does not match dispatch producer" in error for error in result2["errors"])


def test_validate_handoff_cli_rejects_project_local_or_unpinned_index(tmp_path, capsys):
    from scripts.promkes_v2.cli import main
    from scripts.promkes_v2.common import sha256_bytes, sha256_json
    from test_v2_acceptance import valid_handoff
    project = tmp_path / "project"; project.mkdir()
    in_file = project / "in.json"; in_file.write_text('{"a":1}', encoding="utf-8")
    out_file = project / "out.json"; out_file.write_text('{"b":1}', encoding="utf-8")
    h = valid_handoff()
    h["input_refs"][0]["content_hash"] = sha256_bytes(in_file.read_bytes())
    h["outputs"][0]["content_hash"] = sha256_bytes(out_file.read_bytes())
    h["payload_hash"] = sha256_json(h, omit=("payload_hash",))
    handoff = project / "handoff.json"; handoff.write_text(json.dumps(h), encoding="utf-8")
    index = {"ART-IN-1": {"path": str(in_file), "owner_skill_id": "S01"},
             "ART-OUT-1": {"path": str(out_file), "owner_skill_id": "S03"}}
    local_index = project / "artifact-index.json"; local_index.write_text(json.dumps(index), encoding="utf-8")
    code = main(["validate-handoff", str(handoff), "--artifact-index", str(local_index),
                 "--artifact-index-sha256", sha256_bytes(local_index.read_bytes()),
                 "--project-root", str(project), "--expected-producer", "S03"])
    result = json.loads(capsys.readouterr().out)
    assert code == 1 and any("externally managed outside" in error for error in result["errors"])


def test_all_public_skill_modules_link_to_universal_handoff_contract():
    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    assert len(skill_files) == 15
    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        assert "## V2 Universal Handoff Contract" in text, path
        assert "handoff-envelope.schema.json" in text, path
    for dirname in ("health-evidence-safety-auditor", "audience-campaign-strategy",
                    "story-screenplay-architect", "visual-identity-art-direction",
                    "storyboard-cinematography", "animation-motion-design", "continuity-guardian"):
        path = ROOT / "skills" / dirname / "references/v2-operational-protocol.md"
        assert path.is_file() and "## Acceptance" in path.read_text(encoding="utf-8")
    assert (ROOT / "skills/editing-postproduction/references/s10-two-lane-contract.md").is_file()


def test_ci_workflow_runs_v2_acceptance_and_full_regression():
    import yaml
    workflow_path = ROOT / ".github/workflows/v2-acceptance.yml"
    workflow = yaml.load(workflow_path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    assert workflow["name"] == "Promkes V2 Acceptance and Regression"
    steps = workflow["jobs"]["acceptance-and-regression"]["steps"]
    runs = "\n".join(step.get("run", "") for step in steps)
    assert "tests/test_v2_acceptance.py" in runs
    assert "python -m pytest" in runs and " -q tests" in runs
    assert "-p no:cacheprovider" in runs and "PYTHONDONTWRITEBYTECODE=1" in runs
    assert any(step.get("name") == "Remove transient test caches before package validation" for step in steps)
    assert "validate_release_consistency.py" in runs


def test_budget_project_cannot_downgrade_required_categories_from_signed_policy():
    from scripts.promkes_v2.common import sha256_json
    profile = {"status": "APPROVED", "profile_id": "PROFILE-CATEGORIES", "approved_by": "OPS",
               "approval_ref": "APR-CAT", "route": "PROGRAMMATIC_RENDER",
               "ceilings": {"provider_cost": 10, "render_seconds": 100}}
    trusted = {"PROFILE-CATEGORIES": {"route": "PROGRAMMATIC_RENDER", "content_hash": sha256_json(profile),
                                       "required_categories": ["provider_cost", "render_seconds"]}}
    result = evaluate_resource_budget("PROGRAMMATIC_RENDER", profile,
                                      {"provider_cost": 1, "render_seconds": 10}, set(),
                                      trusted_profile_records=trusted)
    assert result["status"] == "BLOCKED"
    assert "required resource categories differ" in result["reason"]


def test_handoff_artifact_path_cannot_escape_declared_project_root(tmp_path):
    from scripts.promkes_v2.handoff import validate_handoff
    from scripts.promkes_v2.common import sha256_bytes
    from test_v2_acceptance import valid_handoff, SCHEMA
    project = tmp_path / "project"; project.mkdir()
    outside = tmp_path / "outside.json"; outside.write_text('{"ok":true}', encoding="utf-8")
    digest = sha256_bytes(outside.read_bytes())
    h = valid_handoff()
    for ref in h["input_refs"] + h["outputs"]: ref["content_hash"] = digest
    h["payload_hash"] = __import__("scripts.promkes_v2.common", fromlist=["sha256_json"]).sha256_json(h, omit=("payload_hash",))
    index = {"ART-IN-1": {"path": outside, "content_hash": digest, "owner_skill_id": "S01"},
             "ART-OUT-1": {"path": outside, "content_hash": digest, "owner_skill_id": "S03"}}
    errors = validate_handoff(h, SCHEMA, expected_producer="S03", artifact_index=index, artifact_root=project)
    assert any("artifact path escapes project root" in error for error in errors)


def test_handoff_rejects_untrusted_producer_identity_from_envelope():
    from scripts.promkes_v2.handoff import validate_handoff
    from test_v2_acceptance import valid_handoff, SCHEMA
    errors = validate_handoff(valid_handoff("S04"), SCHEMA, expected_producer="S03")
    assert any("does not match dispatch producer" in error for error in errors)
