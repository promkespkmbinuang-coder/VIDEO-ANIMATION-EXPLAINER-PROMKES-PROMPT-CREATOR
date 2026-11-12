#!/usr/bin/env python3
"""Fail-closed release consistency and package hygiene validator."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

EXPECTED = {
    "master-orchestrator",
    "source-asset-intelligence",
    "health-evidence-safety-auditor",
    "audience-campaign-strategy",
    "story-screenplay-architect",
    "visual-identity-art-direction",
    "storyboard-cinematography",
    "animation-motion-design",
    "ai-video-reference-engineering",
    "voice-sound-design",
    "editing-postproduction",
    "social-accessibility-distribution",
    "quality-assurance-controller",
    "continuity-guardian",
    "conversation-release-audit",
}
CACHE = {".pytest_cache","__pycache__",".mypy_cache",".ruff_cache",".venv","node_modules"}
IGNORE = {".pytest_cache/","__pycache__/","*.py[cod]",".venv/","build/","node_modules/"}

class DuplicateKey(ValueError): pass

def _pairs(pairs: list[tuple[str,Any]]) -> dict[str,Any]:
    out={}
    for k,v in pairs:
        if k in out: raise DuplicateKey("duplicate JSON key: "+k)
        out[k]=v
    return out

def strict_json(path: Path):
    try: return json.loads(path.read_text(encoding="utf-8"),object_pairs_hook=_pairs)
    except Exception as exc: raise ValueError(f"{path}: {exc}") from exc

def validate_release(root: Path) -> list[str]:
    root=root.resolve(); errors=[]
    try:
        a=strict_json(root/"plugin.json"); b=strict_json(root/".codex-plugin/plugin.json")
    except ValueError as exc: return [str(exc)]
    for p in root.rglob("*.json"):
        try: strict_json(p)
        except ValueError as exc: errors.append(str(exc))
    for k in ("name","version","description","skills","author","keywords"):
        if a.get(k)!=b.get(k): errors.append("manifest parity mismatch: "+k)
    version=a.get("version")
    if not isinstance(version,str) or not all(part.isdigit() for part in version.split(".")) or len(version.split("."))!=3:
        errors.append("invalid strict SemVer")
    ia=a.get("extensions",{}).get("com.openai",{}).get("interface",{})
    ib=b.get("interface",{})
    for k in ("displayName","shortDescription","longDescription","developerName","category","capabilities","defaultPrompt"):
        if ia.get(k)!=ib.get(k): errors.append("interface parity mismatch: "+k)
    if not isinstance(ia.get("shortDescription"),str) or not 1<=len(ia["shortDescription"])<=30:
        errors.append("shortDescription must be 1..30 characters")
    skills=sorted((root/"skills").glob("*/SKILL.md"))
    actual={p.parent.name for p in skills}
    if actual!=EXPECTED: errors.append(f"skill inventory mismatch: missing={sorted(EXPECTED-actual)} extra={sorted(actual-EXPECTED)}")
    if len(skills)!=15: errors.append(f"expected 15 numbered GitHub modules, found {len(skills)}")
    for p in skills:
        lines=p.read_text(encoding="utf-8").splitlines()
        if len(lines)<3 or lines[0]!="---" or not lines[1].startswith("name: "):
            errors.append("invalid skill frontmatter: "+str(p.relative_to(root)))
        elif lines[1].split(":",1)[1].strip().strip("'\"")!=p.parent.name:
            errors.append("skill name/directory mismatch: "+str(p.relative_to(root)))
    bridge=root/"skills/master-orchestrator/references/s14-integration-contract.md"
    if not bridge.is_file(): errors.append("M00/S14 integration contract missing")
    m00=root/"skills/master-orchestrator/SKILL.md"
    if not m00.is_file():
        errors.append("M00 master-orchestrator skill missing")
    else:
        m00_text=m00.read_text(encoding="utf-8").lower()
        required=("conversation-release-audit/skill.md","references/s14-integration-contract.md","references/m00-s14-mandate.md","before any version audit","s14")
        if any(token not in m00_text for token in required):
            errors.append("M00 must directly mandate and link S14 skill, entrypoint and handoff contracts")
    register_path=root/"docs/conversation-context-register-v4.1.2.json"
    if not register_path.is_file():
        errors.append("V4.1.2 conversation context register missing")
    else:
        try:
            register=strict_json(register_path)
            if register.get("context_version")!=version: errors.append("conversation context register version mismatch")
            if not register.get("coverage_boundary"): errors.append("conversation context register coverage boundary missing")
        except ValueError as exc: errors.append(str(exc))
    readme=(root/"README.md").read_text(encoding="utf-8")
    changelog=(root/"CHANGELOG.md").read_text(encoding="utf-8")
    if not readme.splitlines() or version not in readme.splitlines()[0]: errors.append("README title/version mismatch")
    if not any(line=="## "+version or line.startswith("## "+version+" ") for line in changelog.splitlines()):
        errors.append("CHANGELOG version entry missing")
    ig=root/".gitignore"
    if not ig.is_file(): errors.append(".gitignore missing")
    else:
        rules={x.strip() for x in ig.read_text(encoding="utf-8").splitlines()}
        for rule in IGNORE-rules: errors.append(".gitignore rule missing: "+rule)
    for p in root.rglob("*"):
        if p.is_file():
            rel=p.relative_to(root)
            if any(x in CACHE for x in rel.parts) or p.suffix.lower() in {".pyc",".pyo"}:
                errors.append("cache/bytecode must not be packaged: "+str(rel))
    return errors

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--root",type=Path,default=Path.cwd());args=ap.parse_args(argv)
    errors=validate_release(args.root)
    if errors: print(json.dumps({"status":"FAIL","errors":errors},indent=2));return 1
    print(json.dumps({"status":"PASS","scope":"static package hygiene only"},indent=2));return 0
if __name__=="__main__": raise SystemExit(main())
