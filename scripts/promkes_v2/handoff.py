from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from .common import sha256_json, sha256_bytes, resolved_inside

SKILL_IDS = {"M00", *(f"S{i:02d}" for i in range(1, 15))}
VALID_STATUSES = {"DRAFT", "PROPOSED", "IN_PROGRESS", "PASS", "PARTIAL", "NOT_RUN", "NOT_VERIFIED",
                  "NOT_APPLICABLE", "BLOCKED", "STALE", "INVALIDATED", "APPROVED", "REJECTED"}


def structural_errors(handoff: dict, schema_path: Path) -> list[str]:
    try:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(handoff), key=lambda e: list(map(str, e.absolute_path)))
    except Exception as exc:
        return [f"schema load/validation error: {type(exc).__name__}: {exc}"]
    return [f"/{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in errors]


def validate_handoff(handoff: dict, schema_path: Path, *,
                     expected_producer: str | None = None,
                     artifact_index: dict[str, dict] | None = None,
                     artifact_root: Path | None = None,
                     dependency_statuses: dict[str, str] | None = None) -> list[str]:
    errors = structural_errors(handoff, schema_path)
    if errors:
        return errors
    dependency_statuses = dependency_statuses or {}
    producer = handoff["skill_id"]
    if not expected_producer:
        errors.append("/skill_id: expected producer identity from M00 dispatch context is required")
    elif producer != expected_producer:
        errors.append(f"/skill_id: envelope producer {producer} does not match dispatch producer {expected_producer}")
    if not artifact_index:
        errors.append("/artifact_index: external artifact index is required for semantic handoff validation")
        artifact_index = {}

    calculated = sha256_json(handoff, omit=("payload_hash",))
    if calculated.lower() != handoff["payload_hash"].lower():
        errors.append("/payload_hash: digest does not match canonical handoff payload")

    for direction in ("input_refs", "outputs"):
        for i, ref in enumerate(handoff[direction]):
            if ref["status"] in {"BLOCKED", "INVALIDATED", "STALE"} and direction == "input_refs":
                errors.append(f"/{direction}/{i}/status: downstream cannot consume {ref['status']} prerequisite")
            record = artifact_index.get(ref["ref_id"])
            if record is None:
                errors.append(f"/{direction}/{i}/ref_id: unknown artifact {ref['ref_id']}")
                continue
            if record is not None:
                actual_hash = record.get("content_hash")
                if actual_hash is not None and (not isinstance(actual_hash, str)
                                                or actual_hash.lower() != ref["content_hash"].lower()):
                    errors.append(f"/{direction}/{i}/content_hash: referenced artifact hash mismatch or invalid type")
                path = record.get("path")
                if not path:
                    errors.append(f"/{direction}/{i}/content_ref: artifact byte path is required for semantic validation")
                else:
                    try:
                        artifact_path = Path(path)
                        if artifact_root is not None and not resolved_inside(artifact_path, Path(artifact_root)):
                            errors.append(f"/{direction}/{i}/content_ref: artifact path escapes project root")
                            continue
                        actual = sha256_bytes(artifact_path.read_bytes())
                        if actual.lower() != ref["content_hash"].lower():
                            errors.append(f"/{direction}/{i}/content_hash: file bytes mismatch")
                    except (OSError, TypeError, ValueError):
                        errors.append(f"/{direction}/{i}/content_ref: artifact bytes unavailable or invalid path")
                declared_owner = record.get("owner_skill_id")
                ref_owner = ref.get("owner_skill_id")
                if declared_owner and ref_owner and declared_owner != ref_owner:
                    errors.append(f"/{direction}/{i}/owner_skill_id: envelope owner differs from artifact registry owner")
                if direction == "outputs" and declared_owner and declared_owner != producer:
                    errors.append(f"/outputs/{i}/owner_skill_id: producer {producer} cannot own {declared_owner}'s artifact")

    dependency_targets = set()
    for i, trace in enumerate(handoff["trace_links"]):
        for ref_field in ("from_ref", "to_ref"):
            ref_id = trace[ref_field]
            if ref_id not in artifact_index:
                errors.append(f"/trace_links/{i}/{ref_field}: unknown artifact reference {ref_id}")
        if trace["relation"] == "DEPENDS_ON":
            dependency_targets.add(trace["to_ref"])
    for ref_id in sorted(dependency_targets):
        if ref_id not in dependency_statuses:
            errors.append(f"/dependency_statuses/{ref_id}: required upstream dependency status is missing")
        elif dependency_statuses[ref_id] not in {"PASS", "APPROVED"}:
            errors.append(f"/dependency_statuses/{ref_id}: upstream dependency status {dependency_statuses[ref_id]} is not eligible for consumption")

    for i, decision in enumerate(handoff["decisions"]):
        domain = decision["domain"].upper()
        owner = decision["decision_owner_skill_id"]
        status = decision["decision_status"]
        if domain in {"CLINICAL_APPROVAL", "MEDICAL_APPROVAL"}:
            if owner != "HUMAN":
                errors.append(f"/decisions/{i}: clinical approval belongs to an authorized human, not {owner}")
            if producer != "S02" and status in {"LOCKED", "ACCEPTED"}:
                errors.append(f"/decisions/{i}: non-S02 producer cannot lock clinical evidence decision")
        if domain in {"INDEPENDENT_QA", "MEDIA_QA", "RELEASE_QA"}:
            if producer != "S12" or owner != "S12":
                errors.append(f"/decisions/{i}: independent QA is owned and issued by S12 only")

    if any(status in {"BLOCKED", "INVALIDATED", "STALE"} for status in dependency_statuses.values()):
        errors.append("/input_refs: a required upstream dependency is BLOCKED/INVALIDATED/STALE")
    if handoff["status"] == "COMPLETE" and not handoff["outputs"]:
        errors.append("/outputs: COMPLETE handoff requires at least one output artifact")
    return errors


def can_consume_handoff(handoff: dict) -> tuple[bool, str]:
    if handoff.get("status") != "COMPLETE":
        return False, f"producer handoff status is {handoff.get('status')}; recipient must not continue as complete"
    blocked = [r.get("ref_id") for r in handoff.get("input_refs", [])
               if r.get("status") in {"BLOCKED", "INVALIDATED", "STALE"}]
    if blocked:
        return False, f"blocked prerequisites: {blocked}"
    return True, "handoff is structurally eligible; recipient still performs semantic review"
