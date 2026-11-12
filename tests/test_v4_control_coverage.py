import json
from pathlib import Path

from scripts.v4_gate_engine import CONTROL_IDS, GATE_ORDER


def test_every_control_has_explicit_positive_and_negative_test_mapping():
    root = Path(__file__).resolve().parents[1]
    mapping = json.loads((root / "tests/v4-control-test-map.json").read_text(encoding="utf-8"))
    defined_controls = {control for gate in GATE_ORDER for control in CONTROL_IDS[gate]}
    assert set(mapping) == defined_controls
    test_source = (root / "tests/test_v4_gate_engine.py").read_text(encoding="utf-8")
    for control_id, test_names in mapping.items():
        assert len(test_names) >= 2, f"{control_id} needs positive and negative test mapping"
        assert test_names[0] == "test_all_eight_gates_pass_for_complete_synthetic_fixture", control_id
        for test_name in test_names:
            assert f"def {test_name}(" in test_source, f"{control_id} maps to missing test {test_name}"
