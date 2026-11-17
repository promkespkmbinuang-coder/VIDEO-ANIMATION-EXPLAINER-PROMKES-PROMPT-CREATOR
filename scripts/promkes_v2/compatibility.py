from __future__ import annotations

import json
import re
from pathlib import Path


REQUIRED_SKILL_DIRS = {
    "master-orchestrator", "source-asset-intelligence", "health-evidence-safety-auditor",
    "audience-campaign-strategy", "story-screenplay-architect", "visual-identity-art-direction",
    "storyboard-cinematography", "animation-motion-design", "ai-video-reference-engineering",
    "voice-sound-design", "editing-postproduction", "social-accessibility-distribution",
    "quality-assurance-controller", "continuity-guardian", "conversation-release-audit",
}


def _json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _skill_frontmatter(path: Path) -> tuple[str, str]:
    text = Path(path).read_text(encoding="utf-8")
    m = re.match(r"---\s*\nname:\s*([^\n]+)\n(?:description:\s*([^\n]+))?", text)
    if not m:
        raise ValueError(f"invalid skill frontmatter: {path}")
    return m.group(1).strip().strip("'\""), (m.group(2) or "").strip().strip("'\"")


def compare_compatibility(baseline_root: Path, candidate_root: Path) -> list[str]:
    baseline_root, candidate_root = Path(baseline_root), Path(candidate_root)
    errors = []
    for name in ("plugin.json", ".codex-plugin/plugin.json"):
        old, new = _json(baseline_root / name), _json(candidate_root / name)
        for key in ("name", "version", "description", "skills", "author", "keywords"):
            if old.get(key) != new.get(key):
                errors.append(f"{name}: non-additive manifest change at {key}")
    old_dirs = {p.parent.name for p in (baseline_root / "skills").glob("*/SKILL.md")}
    new_dirs = {p.parent.name for p in (candidate_root / "skills").glob("*/SKILL.md")}
    if old_dirs != new_dirs or old_dirs != REQUIRED_SKILL_DIRS:
        errors.append(f"skill inventory/paths changed: baseline={sorted(old_dirs)} candidate={sorted(new_dirs)}")
    for dirname in sorted(old_dirs & new_dirs):
        old_path = baseline_root / "skills" / dirname / "SKILL.md"
        new_path = candidate_root / "skills" / dirname / "SKILL.md"
        try:
            old_name, old_desc = _skill_frontmatter(old_path)
            new_name, new_desc = _skill_frontmatter(new_path)
        except ValueError as exc:
            errors.append(str(exc)); continue
        if old_name != new_name:
            errors.append(f"{dirname}: skill name/identity changed")
        if old_desc != new_desc:
            errors.append(f"{dirname}: trigger/description changed without migration")
    # Existing public output states are preserved in M00.
    old_m00 = (baseline_root / "skills/master-orchestrator/SKILL.md").read_text(encoding="utf-8")
    new_m00 = (candidate_root / "skills/master-orchestrator/SKILL.md").read_text(encoding="utf-8")
    states = ("BLUEPRINT_ONLY", "REFERENCE_READY", "RENDER_READY", "RENDERED_PARTIALLY_VERIFIED", "RENDERED_VERIFIED", "BLOCKED")
    for state in states:
        if state in old_m00 and state not in new_m00:
            errors.append(f"M00 existing output state removed: {state}")
    return errors
