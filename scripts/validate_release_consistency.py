#!/usr/bin/env python3
"""Strict cross-manifest and release-document consistency checks."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any

class DuplicateJSONKeyError(ValueError):
    pass

def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result

def load_strict_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys)
    except (OSError, json.JSONDecodeError, DuplicateJSONKeyError) as exc:
        raise ValueError(f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return value

def validate_release(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = load_strict_json(root / "plugin.json")
        compat = load_strict_json(root / ".codex-plugin" / "plugin.json")
    except ValueError as exc:
        return [str(exc)]
    for key in ("name", "version", "description", "skills"):
        if manifest.get(key) != compat.get(key):
            errors.append(f"manifest parity mismatch for {key}")
    version = manifest.get("version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append(f"invalid semantic version: {version!r}")
    else:
        try:
            readme = (root / "README.md").read_text(encoding="utf-8")
            changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(str(exc))
        else:
            first_line = readme.splitlines()[0] if readme.splitlines() else ""
            if version not in first_line:
                errors.append(f"README first line does not identify release {version}")
            if not re.search(rf"^##\s+{re.escape(version)}(?:\s|$)", changelog, re.MULTILINE):
                errors.append(f"CHANGELOG has no top-level entry for {version}")
    root_interface = manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
    codex_interface = compat.get("interface", {})
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category", "defaultPrompt"):
        if root_interface.get(key) != codex_interface.get(key):
            errors.append(f"interface parity mismatch for {key}")
    if not root_interface.get("displayName"):
        errors.append("OpenAI interface displayName is required")
    return errors

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    errors = validate_release(args.root.resolve())
    if errors:
        print(json.dumps({"status":"FAIL","errors":errors},ensure_ascii=False,indent=2))
        return 1
    print(json.dumps({"status":"PASS","root":str(args.root.resolve())},ensure_ascii=False,indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
