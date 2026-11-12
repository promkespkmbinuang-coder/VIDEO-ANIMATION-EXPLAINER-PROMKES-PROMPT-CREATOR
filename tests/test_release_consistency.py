from __future__ import annotations
import json
from pathlib import Path
import pytest
from scripts.validate_release_consistency import load_strict_json, validate_release

def _package(root: Path):
    (root / ".codex-plugin").mkdir(parents=True)
    interface={"displayName":"Example V4.0.4","shortDescription":"Example","longDescription":"Evidence controls","developerName":"Publisher","category":"Healthcare","defaultPrompt":["Run checks."]}
    common={"name":"example","version":"4.0.4","description":"Example","skills":"./skills"}
    (root/"plugin.json").write_text(json.dumps({**common,"extensions":{"com.openai":{"interface":interface}}}),encoding="utf-8")
    (root/".codex-plugin"/"plugin.json").write_text(json.dumps({**common,"interface":interface}),encoding="utf-8")
    (root/"README.md").write_text("# Example V4.0.4\n",encoding="utf-8")
    (root/"CHANGELOG.md").write_text("# Changelog\n\n## 4.0.4 — update\n",encoding="utf-8")

def test_release_manifests_and_docs_are_consistent(tmp_path: Path):
    _package(tmp_path)
    assert validate_release(tmp_path)==[]

def test_duplicate_json_keys_are_rejected(tmp_path: Path):
    _package(tmp_path)
    path=tmp_path/"plugin.json"
    path.write_text('{"name":"a","name":"b"}',encoding="utf-8")
    with pytest.raises(ValueError,match="duplicate JSON key"):
        load_strict_json(path)

def test_root_codex_version_mismatch_is_reported(tmp_path: Path):
    _package(tmp_path)
    path=tmp_path/".codex-plugin"/"plugin.json"
    data=json.loads(path.read_text(encoding="utf-8"))
    data["version"]="4.0.3"
    path.write_text(json.dumps(data),encoding="utf-8")
    assert any("version" in error for error in validate_release(tmp_path))
