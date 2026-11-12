from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def test_conversation_context_register_matches_schema_and_package_version():
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    version = manifest["version"]
    schema = json.loads((ROOT / "schemas/v4/conversation-context.schema.json").read_text(encoding="utf-8"))
    register_path = ROOT / f"docs/conversation-context-register-v{version}.json"
    register = json.loads(register_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(register),
        key=lambda error: list(error.path),
    )
    assert not errors, "\\n".join(f"{list(error.path)}: {error.message}" for error in errors)
    assert register["context_version"] == version
    ids = [row["ctx_id"] for row in register["records"]]
    assert len(ids) == len(set(ids)), "CTX IDs must be unique"


def test_context_register_keeps_static_design_and_social_performance_scoped():
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    register = json.loads((ROOT / f"docs/conversation-context-register-v{manifest['version']}.json").read_text(encoding="utf-8"))
    by_id = {row["ctx_id"]: row for row in register["records"]}
    assert "1080×1350" in by_id["CTX-DESIGN-008"]["statement"]
    assert "do not define video" in by_id["CTX-DESIGN-008"]["scope"]
    assert "not guaranteed" in by_id["CTX-DIST-020"]["scope"]
    assert by_id["CTX-DIST-020"]["classification"] == "EXPLICIT"
    assert by_id["CTX-UNKNOWN-019"]["classification"] == "UNKNOWN"
