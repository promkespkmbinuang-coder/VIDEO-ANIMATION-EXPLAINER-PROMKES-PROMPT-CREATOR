from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_acceptance_coverage_ledger_matches_all_scenario_specs():
    source = json.loads((ROOT / "tests/acceptance-cases.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    ledger = json.loads((ROOT / f"docs/acceptance-coverage-v{manifest['version']}.json").read_text(encoding="utf-8"))
    source_ids = [case["test_id"] for case in source["cases"]]
    ledger_ids = [case["test_id"] for case in ledger["cases"]]
    assert len(source_ids) == 45
    assert len(source_ids) == len(set(source_ids))
    assert ledger["total_cases"] == len(source_ids)
    assert ledger_ids == source_ids
    assert all(case["specification_status"] == "NOT_RUN" for case in source["cases"])
    assert all(case["execution_status"] == "NOT_RUN" for case in ledger["cases"])
    assert all(case["matching_execution_evidence"] is None for case in ledger["cases"])


def test_aggregate_pytest_does_not_close_acceptance_cases():
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    ledger = json.loads((ROOT / f"docs/acceptance-coverage-v{manifest['version']}.json").read_text(encoding="utf-8"))
    evidence = ledger["pytest_evidence"]
    assert evidence["conclusion"] == "SUCCESS"
    assert "not evidence" in evidence["scope"]
    assert ledger["execution_status"] == "NOT_RUN"
