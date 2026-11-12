from __future__ import annotations
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_gate_engine_has_no_duplicate_top_level_definitions():
    tree = ast.parse((ROOT/"scripts/v4_gate_engine.py").read_text(encoding="utf-8"))
    names = [node.name for node in tree.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
    duplicates = sorted({name for name in names if names.count(name)>1})
    assert duplicates == [], f"Duplicate top-level definitions: {duplicates}"
    assert names.count("main") == 1
