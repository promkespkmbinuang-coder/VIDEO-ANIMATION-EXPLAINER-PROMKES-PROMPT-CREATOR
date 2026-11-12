from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

def test_conversation_context_register_matches_schema():
    schema = json.loads((ROOT/"schemas/v4/conversation-context.schema.json").read_text(encoding="utf-8"))
    register = json.loads((ROOT/"docs/conversation-context-register-v4.1.2.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(register), key=lambda e: list(e.path))
    assert not errors, "\\n".join(f"{list(e.path)}: {e.message}" for e in errors)
    ids = [row["ctx_id"] for row in register["records"]]
    assert len(ids) == len(set(ids)), "CTX IDs must be unique"
    assert register["coverage_boundary"].startswith("Compiled from the current conversation")

def test_register_is_not_clinical_evidence_or_raw_history():
    register = json.loads((ROOT/"docs/conversation-context-register-v4.1.2.json").read_text(encoding="utf-8"))
    assert "Raw full text" in register["coverage_boundary"]
    assert any("not clinical evidence" in note.lower() for note in register["notes"])
