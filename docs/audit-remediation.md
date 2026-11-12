# Audit remediation record — v1.2.0

## Disposition

This release addresses static package integrity, traceability contracts, GitHub source preparation, documentation freshness, and publisher metadata. It does **not** convert unavailable or unexecuted runtime/render tests into passes. Public distribution readiness remains **HOLD** until the external evidence and publisher decisions listed below are closed.

## Finding closure map

| Finding | Remediation in v1.2.0 | Evidence required to close fully |
|---|---|---|
| DEF-GH-001 — source absent from repository | Complete source package staged to a dedicated review branch; keep `main` unchanged until review | Verify all files on GitHub, green CI, merge approval |
| Validator uses YAML regex | Strict `yaml.SafeLoader`-based parser with duplicate-key rejection | GitHub Actions run on the submitted commit |
| Skill folder/name mismatch unchecked | Enforce `frontmatter.name == directory name` and uniqueness | Static validator PASS |
| Compatibility manifest unchecked | Parse `.codex-plugin/plugin.json` and compare name/version/publisher with root manifest | Static validator PASS |
| Supporting references unchecked | Resolve local Markdown links, reference definitions, HTML href/src and heading anchors; lychee workflow checks URLs | Validator and link workflow PASS |
| Traceability only in docs | Add machine-readable 1:1 `tests/traceability.json` mapping for all 58 test IDs, with requirement_ids, owner_skill, dependency_ids and output_ids | Validator coverage PASS; dynamic cases executed separately |
| DEF-QA-002 — incomplete requirement/test relation | Catalog includes REQ-01–10, NFR-01–03 and REQ-REF-01–09; orphan/unknown references rejected | Static validator PASS and change-impact review on changes |
| DEF-PUB-001 — license absent | Rights gate documented; no license invented or added without publisher decision | Publisher rights review and explicit license selection |
| DEF-DOC-001 — stale Cursor URL | Replaced with current official Cursor Agent Skills documentation URL | Lychee workflow and periodic URL review |
| DEF-META-001 — publisher metadata differs | Root and compatibility author/developer metadata synchronized to Promkes pkm binuang | Static manifest comparison PASS |
| Domain repair routing not runtime-tested | M00 ownership and S12 defect-routing evidence remain specified separately | Host runtime trace showing dispatch, owner repair and M00 re-integration |
| Health evidence model only statically reviewed | Keep source material separate from verified claim; add fixture protocol and status labels | Run health fixtures with evidence source locators and independent clinical review |
| MCG continuity not output-tested | Canonical Guide versions and lock references remain explicit | Multi-scene character/setting/reference regression outputs reviewed |
| Render consistency not tested | Define separate renderer/artifact QA gate | Actual rendered video/audio/subtitle/overlay package and reviewer record |

## Validation layers

1. Package/static: manifests, YAML, skill identity, local link integrity, test registry and traceability.
2. Host runtime: skill discovery, invocation, reference loading, tool access, handoff and defect routing on each named host/version.
3. External reference model: prompt acceptance, image/reference generation, identity stability, aspect ratio and asset file provenance.
4. Renderer integration: target schema, asset resolution, frame/time conversion, layers, typography, subtitle and audio mapping.
5. Rendered artifact QA: visual continuity, anatomical plausibility, visual/narrative consistency, audio/subtitle sync, exact text/logo and duration.
6. Human approval: health authority, institutional brand/data owner and release authority approvals.

A pass at one layer never implies a pass at a later layer.

## Current test truth

- 45 baseline acceptance cases: specifications only; `NOT_RUN`.
- 13 Prompt-to-Reference cases: specifications only; `NOT_RUN`.
- Host runtime tests: `NOT_RUN`.
- External AI reference-model tests: `NOT_RUN`.
- Renderer integration: `NOT_RUN`.
- Video/audio artifact QA: `BLOCKED` until real renders are supplied.
- Clinical/health fixture review: `NOT_RUN` until representative campaign fixtures and qualified reviewer evidence exist.
- Human approval: `NOT_RUN`.

## Remaining release blockers

1. Publisher decision on a license after asset/rights review.
2. GitHub review branch validation and merge to `main` after maintainer review.
3. Five host/runtime test records with exact versions and raw evidence.
4. External reference model tests and renderer integration test.
5. Actual render artifact QA and human approval for representative public-health output.
