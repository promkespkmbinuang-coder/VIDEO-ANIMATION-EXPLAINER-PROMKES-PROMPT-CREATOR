from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

CONTROL_AUX: dict[str, dict[str, Any]] = {
    "V4-CTL-001": {"risk": "HIGH", "test_ids": ["TST-009", "TST-010"], "owner_skill_ids": ["S01", "S02"]},
    "V4-CTL-002": {"risk": "CRITICAL", "test_ids": ["TST-025", "TST-026", "TST-029", "TST-030"], "owner_skill_ids": ["S02", "S04"]},
    "V4-CTL-003": {"risk": "CRITICAL", "test_ids": ["TST-002", "TST-003", "TST-022"], "owner_skill_ids": ["S02", "M00"]},
    "V4-CTL-004": {"risk": "HIGH", "test_ids": ["TST-009", "TST-011"], "owner_skill_ids": ["S01", "S02"]},
    "V4-CTL-005": {"risk": "HIGH", "test_ids": ["TST-032", "TST-033"], "owner_skill_ids": ["S06", "M00"]},
    "V4-CTL-006": {"risk": "MEDIUM", "test_ids": ["TST-036"], "owner_skill_ids": ["S06", "S13"]},
    "V4-CTL-007": {"risk": "HIGH", "test_ids": ["TST-012", "TST-013", "TST-037"], "owner_skill_ids": ["M00", "S13"]},
    "V4-CTL-008": {"risk": "HIGH", "test_ids": ["TST-031", "TST-038"], "owner_skill_ids": ["S08", "S10"]},
    "V4-CTL-009": {"risk": "HIGH", "test_ids": ["TST-020", "TST-040"], "owner_skill_ids": ["M00", "S10"]},
    "V4-CTL-010": {"risk": "HIGH", "test_ids": ["TST-039"], "owner_skill_ids": ["S10", "M00"]},
    "V4-CTL-011": {"risk": "HIGH", "test_ids": ["TST-039", "TST-043"], "owner_skill_ids": ["S10", "M00"]},
    "V4-CTL-012": {"risk": "HIGH", "test_ids": ["TST-031"], "owner_skill_ids": ["S05", "M00"]},
    "V4-CTL-013": {"risk": "HIGH", "test_ids": ["TST-005", "TST-008"], "owner_skill_ids": ["S01", "M00"]},
    "V4-CTL-014": {"risk": "CRITICAL", "test_ids": ["TST-005", "TST-006", "TST-007", "TST-008"], "owner_skill_ids": ["M00", "S01"]},
    "V4-CTL-015": {"risk": "HIGH", "test_ids": ["TST-014", "TST-015"], "owner_skill_ids": ["M00", "S10"]},
    "V4-CTL-016": {"risk": "CRITICAL", "test_ids": ["TST-001", "TST-002", "TST-003", "TST-004"], "owner_skill_ids": ["M00", "HUMAN"]},
    "V4-CTL-017": {"risk": "HIGH", "test_ids": ["TST-018", "TST-019", "TST-023"], "owner_skill_ids": ["M00"]},
    "V4-CTL-018": {"risk": "HIGH", "test_ids": ["TST-012", "TST-013", "TST-037"], "owner_skill_ids": ["M00", "S13"]},
    "V4-CTL-019": {"risk": "HIGH", "test_ids": ["TST-019", "TST-020"], "owner_skill_ids": ["M00", "S12"]},
    "V4-CTL-020": {"risk": "HIGH", "test_ids": ["TST-041", "TST-042"], "owner_skill_ids": ["S12"]},
    "V4-CTL-021": {"risk": "HIGH", "test_ids": ["TST-031", "TST-036"], "owner_skill_ids": ["S05", "S13"]},
}


def _legacy_aliases() -> dict[str, dict]:
    # Historical CTRL identifiers are retained as migration aliases. A declared
    # one-to-many mapping is intentional and not treated as an ambiguous alias.
    return {
        "CTRL-INTAKE-INVENTORY": {"targets": ["V4-CTL-012", "V4-CTL-013"], "mapping_kind": "ONE_TO_MANY", "rationale": "rights and privacy intake controls"},
        "CTRL-PRIVACY-CLASSIFICATION": {"targets": ["V4-CTL-013"], "mapping_kind": "ONE_TO_ONE", "rationale": "privacy classification"},
        "CTRL-RIGHTS-BASIS": {"targets": ["V4-CTL-012"], "mapping_kind": "ONE_TO_ONE", "rationale": "rights clearance"},
        "CTRL-UNTRUSTED-INPUTS": {"targets": ["V4-CTL-014"], "mapping_kind": "ONE_TO_ONE", "rationale": "source firewall"},
        "CTRL-CLAIM-SCHEMA": {"targets": ["V4-CTL-001", "V4-CTL-002"], "mapping_kind": "ONE_TO_MANY", "rationale": "claim source and fail-closed status"},
        "CTRL-SOURCE-PROVENANCE": {"targets": ["V4-CTL-004"], "mapping_kind": "ONE_TO_ONE", "rationale": "source provenance"},
        "CTRL-MATERIAL-CLAIMS": {"targets": ["V4-CTL-002", "V4-CTL-003"], "mapping_kind": "ONE_TO_MANY", "rationale": "materiality and clinical review"},
        "CTRL-CLINICAL-APPROVAL": {"targets": ["V4-CTL-003", "V4-CTL-016"], "mapping_kind": "ONE_TO_MANY", "rationale": "clinical review and signed authority"},
        "CTRL-NARRATIVE-TRACEABILITY": {"targets": ["V4-CTL-002"], "mapping_kind": "ONE_TO_ONE", "rationale": "claim-safe narrative traceability"},
        "CTRL-SAFE-WORDING": {"targets": ["V4-CTL-002"], "mapping_kind": "ONE_TO_ONE", "rationale": "safe wording"},
        "CTRL-CONTINUITY-LOCKS": {"targets": ["V4-CTL-007", "V4-CTL-021"], "mapping_kind": "ONE_TO_MANY", "rationale": "dependency and visual locks"},
        "CTRL-VISUAL-REFERENCES": {"targets": ["V4-CTL-021"], "mapping_kind": "ONE_TO_ONE", "rationale": "visual references"},
        "CTRL-PROMPT-INJECTION": {"targets": ["V4-CTL-014"], "mapping_kind": "ONE_TO_ONE", "rationale": "prompt injection"},
        "CTRL-PROMPT-BOUNDARY": {"targets": ["V4-CTL-014"], "mapping_kind": "ONE_TO_ONE", "rationale": "tool boundary"},
        "CTRL-SCENE-TIMING": {"targets": ["V4-CTL-005"], "mapping_kind": "ONE_TO_ONE", "rationale": "scene timing"},
        "CTRL-MANIFEST-INTEGRITY": {"targets": ["V4-CTL-006", "V4-CTL-007", "V4-CTL-009", "V4-CTL-019"], "mapping_kind": "ONE_TO_MANY", "rationale": "identity, dependencies, hashes and status"},
        "CTRL-CAPABILITY-VERIFICATION": {"targets": ["V4-CTL-010"], "mapping_kind": "ONE_TO_ONE", "rationale": "capability evidence"},
        "CTRL-CODE-STATIC": {"targets": ["V4-CTL-011"], "mapping_kind": "ONE_TO_ONE", "rationale": "renderer/code gate"},
        "CTRL-ARTIFACT-QA": {"targets": ["V4-CTL-019", "V4-CTL-020"], "mapping_kind": "ONE_TO_MANY", "rationale": "artifact status and QA evidence"},
        "CTRL-ACCESSIBILITY-QA": {"targets": ["V4-CTL-020"], "mapping_kind": "ONE_TO_ONE", "rationale": "recorded QA evidence; detailed accessibility remains S12"},
        "CTRL-RELEASE-APPROVAL": {"targets": ["V4-CTL-016", "V4-CTL-017"], "mapping_kind": "ONE_TO_MANY", "rationale": "authorized approval and fail-closed gate"},
    }


def build_control_specs() -> list[dict]:
    # Source of executable adapter identity: the existing V4 engine definition.
    from scripts.v4_gate_engine import CONTROL_REGISTRY, GATE_CONTROLS
    gate_by_control: dict[str, list[str]] = {}
    for gate, ids in GATE_CONTROLS.items():
        for cid in ids:
            gate_by_control.setdefault(cid, []).append(gate)
    rows = []
    for cid, adapter, objective in CONTROL_REGISTRY:
        aux = CONTROL_AUX[cid]
        gates = set(gate_by_control.get(cid, []))
        # The old registry locates firewall at intake; V4 engine also rechecks
        # it at G4. V2 represents both boundaries explicitly.
        if cid == "V4-CTL-014":
            gates.add("G0_INTAKE_OK")
        rows.append({"control_id": cid, "adapter": adapter, "objective": objective,
                     "gates": sorted(gates), **aux})
    return rows


def generate_registry(path: Path) -> dict:
    rows = build_control_specs()
    doc = {"registry_version": "2.0.0", "status": "CANONICAL", "control_count": len(rows),
           "controls": rows, "legacy_aliases": _legacy_aliases(),
           "migration_policy": "Additive aliases only; do not rename public skill IDs, paths, triggers or states."}
    Path(path).write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return doc


def validate_registry(path: Path) -> list[str]:
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"cannot read V2 control registry: {type(exc).__name__}: {exc}"]
    errors = []
    schema_path = Path(__file__).resolve().parents[2] / "schemas/v4/control-registry-v2.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        schema_errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(doc),
                               key=lambda e: list(map(str, e.absolute_path)))
        errors.extend(f"/{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in schema_errors)
    except Exception as exc:
        return [f"cannot load/validate V2 control registry schema: {type(exc).__name__}: {exc}"]
    try:
        expected = {x["control_id"]: x for x in build_control_specs()}
    except Exception as exc:
        return [f"cannot read executable engine specification: {type(exc).__name__}: {exc}"]
    records = doc.get("controls", [])
    got = {r.get("control_id"): r for r in records if isinstance(r, dict)}
    if len(got) != len(records): errors.append("duplicate/malformed control IDs in V2 registry")
    if set(got) != set(expected): errors.append("control ID inventory differs from executable engine")
    for cid in sorted(set(got) & set(expected)):
        if got[cid] != expected[cid]:
            fields = sorted(set(got[cid]) | set(expected[cid]))
            differing = [f for f in fields if got[cid].get(f) != expected[cid].get(f)]
            errors.append(f"{cid} metadata mismatch: {differing}")
    if doc.get("control_count") != len(expected): errors.append("control_count mismatch")
    aliases = doc.get("legacy_aliases", {})
    expected_aliases = _legacy_aliases()
    if set(aliases) != set(expected_aliases):
        errors.append(f"legacy alias inventory mismatch: missing={sorted(set(expected_aliases)-set(aliases))} extra={sorted(set(aliases)-set(expected_aliases))}")
    known = set(expected)
    for alias, spec in aliases.items():
        targets = spec.get("targets", []) if isinstance(spec, dict) else []
        kind = spec.get("mapping_kind") if isinstance(spec, dict) else None
        if not targets: errors.append(f"legacy alias {alias} has no target")
        if set(targets) - known: errors.append(f"legacy alias {alias} maps to unknown controls: {sorted(set(targets)-known)}")
        if len(targets) != len(set(targets)): errors.append(f"legacy alias {alias} repeats a target")
        if len(targets) > 1 and kind != "ONE_TO_MANY": errors.append(f"legacy alias {alias} is ambiguous: explicit ONE_TO_MANY rationale required")
        if len(targets) == 1 and kind != "ONE_TO_ONE": errors.append(f"legacy alias {alias} must be ONE_TO_ONE")
        if not spec.get("rationale"): errors.append(f"legacy alias {alias} lacks migration rationale")
    return errors
