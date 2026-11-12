#!/usr/bin/env python3
"""Strict static validator for the Prompt-to-Reference Promkes skill package.

This validates package structure and traceability contracts only. It does not
execute AI hosts, reference models, renderers, video/audio QA, or human approval.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError as exc:  # fail closed; no regex-only fallback
    raise SystemExit("PyYAML is required. Install requirements-dev.txt first.") from exc

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = 15
EXPECTED_AT = 45
EXPECTED_REF = 13
ERRORS: list[str] = []
WARNINGS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Missing JSON file: {path.relative_to(ROOT)}")
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        fail(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
    return None


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""
    def construct_mapping(self, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in mapping
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    "found an unhashable key", key_node.start_mark
                ) from exc
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    f"duplicate key {key!r}", key_node.start_mark
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def parse_frontmatter(path: Path):
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        fail(f"YAML frontmatter must begin at byte 0: {path.relative_to(ROOT)}")
        return None, raw
    end = raw.find("\n---", 4)
    if end < 0:
        fail(f"YAML frontmatter closing delimiter missing: {path.relative_to(ROOT)}")
        return None, raw
    fm_text = raw[4:end]
    body = raw[end + 4:]
    try:
        fm = yaml.load(fm_text, Loader=UniqueKeySafeLoader)
    except yaml.YAMLError as exc:
        fail(f"Invalid YAML frontmatter in {path.relative_to(ROOT)}: {exc}")
        return None, body
    if not isinstance(fm, dict):
        fail(f"Frontmatter must be a YAML mapping: {path.relative_to(ROOT)}")
        return None, body
    for key in ("name", "description"):
        if not isinstance(fm.get(key), str) or not fm[key].strip():
            fail(f"Frontmatter {key} must be a non-empty string: {path.relative_to(ROOT)}")
    return fm, body


def heading_slug(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    return text


def strip_fenced_code(text: str) -> str:
    out = []
    in_fence = False
    fence_char = None
    fence_len = 0
    for line in text.splitlines():
        m = re.match(r"^\s*(```+|~~~+)", line)
        if m:
            token = m.group(1)
            if not in_fence:
                in_fence, fence_char, fence_len = True, token[0], len(token)
            elif token[0] == fence_char and len(token) >= fence_len:
                in_fence = False
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def markdown_links(text: str):
    text = strip_fenced_code(text)
    candidates = []
    # Inline links and images: [label](target), ![alt](target)
    for m in re.finditer(r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)", text):
        candidates.append(m.group(1))
    # Reference-style link definitions: [id]: target
    for m in re.finditer(r"(?m)^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)", text):
        candidates.append(m.group(1))
    # HTML href/src attributes in supporting references.
    for m in re.finditer(r"(?i)(?:href|src)\s*=\s*[\"\']([^\"\']+)[\"\']", text):
        candidates.append(m.group(1))
    for item in candidates:
        item = item.strip()
        if item.startswith("<") and item.endswith(">"):
            item = item[1:-1]
        yield item.rstrip(".,;:)")


def validate_markdown_links():
    md_files = sorted(ROOT.rglob("*.md"))
    for md in md_files:
        if any(part in {".git", "exports", "build"} for part in md.parts):
            continue
        content = md.read_text(encoding="utf-8")
        slugs = set()
        for line in content.splitlines():
            m = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
            if m:
                base = heading_slug(m.group(1))
                slug = base
                n = 1
                while slug in slugs:
                    n += 1
                    slug = f"{base}-{n}"
                slugs.add(slug)
        for raw_target in markdown_links(content):
            if not raw_target or raw_target.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
                continue
            parts = urlsplit(raw_target)
            target_text = unquote(parts.path)
            if not target_text:
                target = md
            elif target_text.startswith("/"):
                target = (ROOT / target_text.lstrip("/")).resolve()
            else:
                target = (md.parent / target_text).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"Markdown link escapes package root: {raw_target} in {md.relative_to(ROOT)}")
                continue
            if not target.exists():
                fail(f"Broken local Markdown/supporting reference: {raw_target} in {md.relative_to(ROOT)}")
                continue
            fragment = unquote(parts.fragment)
            if fragment and target.is_file() and target.suffix.lower() in {".md", ".markdown"}:
                target_text_content = target.read_text(encoding="utf-8")
                target_slugs = set()
                for line in target_text_content.splitlines():
                    hm = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
                    if hm:
                        base = heading_slug(hm.group(1))
                        slug = base
                        k = 1
                        while slug in target_slugs:
                            k += 1
                            slug = f"{base}-{k}"
                        target_slugs.add(slug)
                if fragment not in target_slugs:
                    fail(f"Broken Markdown anchor #{fragment} in {raw_target} from {md.relative_to(ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary-json", help="Optional path for a machine-readable validation summary")
    args = ap.parse_args()

    required = [
        "plugin.json", ".codex-plugin/plugin.json", "README.md", "CHANGELOG.md",
        "CONTRIBUTING.md", "docs/architecture.md", "docs/platform-compatibility.md",
        "docs/github-publication.md", "docs/requirements-traceability.md",
        "docs/audit-remediation.md", "docs/reference-output-contract.md",
        "tests/acceptance-cases.json", "tests/reference-output-cases.json",
        "tests/traceability.json", "requirements-dev.txt",
    ]
    for rel in required:
        if not (ROOT / rel).is_file():
            fail(f"Missing required file: {rel}")

    manifest = load_json(ROOT / "plugin.json") or {}
    compat = load_json(ROOT / ".codex-plugin/plugin.json") or {}
    compat_ext = compat.get("interface", {}) if isinstance(compat, dict) else {}
    root_author = manifest.get("author", {}) if isinstance(manifest, dict) else {}
    compat_author = compat.get("author", {}) if isinstance(compat, dict) else {}
    version = manifest.get("version")
    if not isinstance(version, str) or not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version):
        fail(f"Root manifest version must be a valid SemVer MAJOR.MINOR.PATCH; found {version!r}")
    if compat.get("version") != version:
        fail("Compatibility manifest version does not match root manifest")
    if compat.get("name") != manifest.get("name"):
        fail("Compatibility manifest name does not match root manifest")
    if root_author != compat_author:
        fail("Publisher author metadata differs between root and compatibility manifests")
    if compat_ext.get("developerName") != root_author.get("name"):
        fail("Compatibility developerName differs from canonical publisher name")
    if not root_author.get("name"):
        fail("Canonical publisher name missing")
    if "Workspace upload" in json.dumps(compat, ensure_ascii=False):
        fail("Stale 'Workspace upload' publisher metadata remains")

    # Canonical skills and strict YAML frontmatter validation.
    skill_dirs = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir()) if (ROOT / "skills").is_dir() else []
    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md")) if (ROOT / "skills").is_dir() else []
    if len(skill_files) != EXPECTED_SKILLS:
        fail(f"Expected {EXPECTED_SKILLS} skills (M00 + S01-S14), found {len(skill_files)}")
    names = set()
    for skill_file in skill_files:
        fm, _ = parse_frontmatter(skill_file)
        if fm is None:
            continue
        name = fm.get("name")
        if name in names:
            fail(f"Duplicate skill name: {name}")
        names.add(name)
        if name != skill_file.parent.name:
            fail(f"Skill name/directory mismatch: {name!r} != {skill_file.parent.name!r}")
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", str(name or "")):
            fail(f"Invalid skill name in {skill_file.relative_to(ROOT)}")
        desc = fm.get("description", "")
        if len(desc) < 20 or len(desc) > 1024:
            fail(f"Skill description length invalid in {skill_file.relative_to(ROOT)}")

    # Both plugin manifests must remain skills-only and schema-compatible.
    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        fail("Root manifest schema declaration invalid/missing")
    if not isinstance(manifest.get("skills"), str) or manifest.get("skills") != "./skills":
        fail("Root manifest skills entry must be ./skills")
    ext = manifest.get("extensions", {}).get("com.openai", {})
    interface = ext.get("interface", {})
    allowed_categories = {"Business & Operations", "Communication", "Creativity", "Data & Analytics", "Developer Tools", "Education & Research", "Entertainment", "Finance", "Healthcare", "Other", "Productivity", "Scientific Research", "Security", "Travel"}
    if interface.get("category") not in allowed_categories:
        fail("Unsupported interface category")
    if len(interface.get("displayName", "")) > 30:
        fail("displayName exceeds 30 characters")
    if len(interface.get("shortDescription", "")) > 30:
        fail("shortDescription exceeds 30 characters")
    if len(interface.get("longDescription", "")) > 4000:
        fail("longDescription exceeds 4000 characters")
    if "apps" in ext and ext.get("apps") is not None:
        fail("Unexpected app binding in skills-only package")
    for forbidden in ("mcp.json", ".app.json"):
        if (ROOT / forbidden).exists():
            fail(f"Unexpected {forbidden} in skills-only package")

    # Acceptance suite counts and immutable execution truth.
    at_suite = load_json(ROOT / "tests/acceptance-cases.json") or {}
    ref_suite = load_json(ROOT / "tests/reference-output-cases.json") or {}
    at_cases = at_suite.get("cases", [])
    ref_cases = ref_suite.get("cases", [])
    if len(at_cases) != EXPECTED_AT:
        fail(f"Expected {EXPECTED_AT} baseline acceptance cases, found {len(at_cases)}")
    if len(ref_cases) != EXPECTED_REF:
        fail(f"Expected {EXPECTED_REF} Prompt-to-Reference cases, found {len(ref_cases)}")
    if at_suite.get("suite_status") != "SPECIFICATION_ONLY_NOT_RUN":
        fail("Baseline suite status must remain SPECIFICATION_ONLY_NOT_RUN until executed")
    if ref_suite.get("suite_status") != "SPECIFICATION_ONLY_NOT_RUN":
        fail("Reference suite status must remain SPECIFICATION_ONLY_NOT_RUN until executed")
    all_cases = at_cases + ref_cases
    test_ids = [case.get("test_id") for case in all_cases]
    if None in test_ids or len(test_ids) != len(set(test_ids)):
        fail("Acceptance test IDs are missing or duplicated across suites")
    # The baseline and Prompt-to-Reference suites intentionally use distinct
    # case schemas. AT cases carry a family and textual input_fixture; REF
    # cases describe the reference contract and do not require those fields.
    suite_requirements = (
        ("baseline", at_cases, ("test_id", "title", "family", "input_fixture", "expected", "oracle", "status")),
        ("reference", ref_cases, ("test_id", "title", "expected", "oracle", "status")),
    )
    for suite_name, cases, required_fields in suite_requirements:
        for case in cases:
            for field in required_fields:
                if not case.get(field):
                    fail(f"Missing {field} in {suite_name} test case {case.get('test_id')}")
            if case.get("status") != "NOT_RUN":
                fail(f"Unexecuted specification must remain NOT_RUN: {case.get('test_id')}")

    # Machine-readable requirement -> test -> owner -> dependency -> output join.
    trace = load_json(ROOT / "tests/traceability.json") or {}
    reqs = {x.get("requirement_id") for x in trace.get("requirements", [])}
    outputs = {x.get("output_id") for x in trace.get("outputs", [])}
    case_map = trace.get("cases", {})
    if set(case_map) != set(test_ids):
        missing = sorted(set(test_ids) - set(case_map))
        extra = sorted(set(case_map) - set(test_ids))
        fail(f"Traceability coverage mismatch; missing={missing}, extra={extra}")
    for test_id, data in case_map.items():
        if not isinstance(data, dict):
            fail(f"Traceability record must be an object: {test_id}")
            continue
        for field in ("requirement_ids", "owner_skill", "dependency_ids", "output_ids"):
            if field not in data:
                fail(f"Traceability field {field} missing for {test_id}")
        if data.get("owner_skill") not in names:
            fail(f"Unknown owner_skill for {test_id}: {data.get('owner_skill')}")
        if not data.get("requirement_ids"):
            fail(f"No requirement_ids for {test_id}")
        for rid in data.get("requirement_ids", []):
            if rid not in reqs:
                fail(f"Unknown requirement {rid} referenced by {test_id}")
        for dep in data.get("dependency_ids", []):
            if dep not in set(test_ids) or dep == test_id:
                fail(f"Unknown or self dependency {dep} referenced by {test_id}")
        if not data.get("output_ids"):
            fail(f"No output_ids for {test_id}")
        for oid in data.get("output_ids", []):
            if oid not in outputs:
                fail(f"Unknown output {oid} referenced by {test_id}")

    # All Markdown, including supporting references, is checked locally.
    validate_markdown_links()
    platform_doc = (ROOT / "docs/platform-compatibility.md").read_text(encoding="utf-8")
    if "docs.cursor.com/context/skills" in platform_doc:
        fail("Obsolete Cursor skills URL remains")
    if "https://cursor.com/docs/skills" not in platform_doc:
        fail("Current official Cursor Skills reference missing")

    if ERRORS:
        print("PACKAGE VALIDATION: FAIL")
        for err in ERRORS:
            print(f" - {err}")
        return 1

    summary = {
        "result": "PASS",
        "scope": "static package validation only",
        "version": version,
        "skills": len(skill_files),
        "acceptance_cases": len(at_cases),
        "reference_cases": len(ref_cases),
        "traceability_records": len(case_map),
        "markdown_files_checked": len(list(ROOT.rglob("*.md"))),
        "dynamic_host_runtime": "NOT_RUN",
        "external_ai_reference_runtime": "NOT_RUN",
        "renderer_integration": "NOT_RUN",
        "video_audio_artifact_qa": "NOT_RUN",
        "human_approval": "NOT_RUN",
    }
    print("PACKAGE VALIDATION: PASS (strict static checks only)")
    print(f"Skills: {summary['skills']} | Acceptance: {summary['acceptance_cases']} | Reference: {summary['reference_cases']} | Traceability: {summary['traceability_records']} | Version: {version}")
    print("Dynamic host/model/renderer/artifact/human tests: NOT RUN; this validator does not imply runtime readiness.")
    if args.summary_json:
        out = Path(args.summary_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
