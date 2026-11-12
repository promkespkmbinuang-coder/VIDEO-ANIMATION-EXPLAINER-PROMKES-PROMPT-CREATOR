from pathlib import Path
import json
from scripts.validate_release_consistency import validate_release

SKILLS={"master-orchestrator","source-asset-intelligence","health-evidence-safety-auditor","audience-campaign-strategy","story-screenplay-architect","visual-identity-art-direction","storyboard-cinematography","animation-motion-design","ai-video-reference-engineering","voice-sound-design","editing-postproduction","social-accessibility-distribution","quality-assurance-controller","continuity-guardian","conversation-release-audit"}

def package(root):
    (root/".codex-plugin").mkdir(parents=True)
    (root/"skills/master-orchestrator/references").mkdir(parents=True)
    iface={"displayName":"Example V4.1.2","shortDescription":"Evidence-gated Promkes","longDescription":"Evidence","developerName":"Publisher","category":"Productivity","capabilities":[],"defaultPrompt":["S14 preflight"]}
    common={"name":"example","version":"4.1.2","description":"Example","skills":"./skills","author":{"name":"Publisher"},"keywords":["example"]}
    (root/"plugin.json").write_text(json.dumps({**common,"$schema":"https://agent-plugins.org/schemas/1.0.0/plugin.schema.json","extensions":{"com.openai":{"interface":iface}}}))
    (root/".codex-plugin/plugin.json").write_text(json.dumps({**common,"interface":iface}))
    (root/"README.md").write_text("# Example V4.1.2\n")
    (root/"CHANGELOG.md").write_text("# Changelog\n\n## 4.1.2 — test\n")
    (root/".gitignore").write_text(".pytest_cache/\n__pycache__/\n*.py[cod]\n.venv/\nbuild/\nnode_modules/\n")
    (root/"skills/master-orchestrator/references/s14-integration-contract.md").write_text("# M00 S14 handoff\n")
    for n in SKILLS:
        p=root/"skills"/n/"SKILL.md";p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(f"---\nname: {n}\ndescription: Valid test skill.\n---\n")
    (root/"skills/master-orchestrator/SKILL.md").write_text(
        "---\\nname: master-orchestrator\\ndescription: M00 orchestrator.\\n---\\n"
        "Before any version audit, apply S14. See conversation-release-audit/SKILL.md, "
        "references/s14-integration-contract.md and references/m00-s14-mandate.md.\\n"
    )
    (root/"docs").mkdir(exist_ok=True)
    (root/"docs/conversation-context-register-v4.1.2.json").write_text(
        json.dumps({"context_version":"4.1.2","coverage_boundary":"test fixture"})
    )

def test_consistent_release(tmp_path):
    package(tmp_path);assert validate_release(tmp_path)==[]

def test_duplicate_json_key_fails(tmp_path):
    package(tmp_path);p=tmp_path/"schema.json";p.write_text('{"x":1,"x":2}')
    assert any("duplicate JSON key" in e for e in validate_release(tmp_path))

def test_short_description_limit_fails(tmp_path):
    package(tmp_path);p=tmp_path/"plugin.json";d=json.loads(p.read_text())
    d["extensions"]["com.openai"]["interface"]["shortDescription"]="This is much longer than thirty characters"
    p.write_text(json.dumps(d))
    assert any("shortDescription" in e for e in validate_release(tmp_path))

def test_cache_file_fails(tmp_path):
    package(tmp_path);p=tmp_path/"tests/__pycache__/x.pyc";p.parent.mkdir(parents=True);p.write_bytes(b"x")
    assert any("cache/bytecode" in e for e in validate_release(tmp_path))

def test_skill_missing_fails(tmp_path):
    package(tmp_path);(tmp_path/"skills/conversation-release-audit/SKILL.md").unlink()
    assert any("skill inventory mismatch" in e for e in validate_release(tmp_path))


def test_m00_must_directly_link_s14_entrypoint(tmp_path):
    package(tmp_path)
    (tmp_path/"skills/master-orchestrator/SKILL.md").write_text(
        "---\\nname: master-orchestrator\\ndescription: M00.\\n---\\nBefore any version audit only.\\n"
    )
    assert any("M00 must directly mandate" in error for error in validate_release(tmp_path))
