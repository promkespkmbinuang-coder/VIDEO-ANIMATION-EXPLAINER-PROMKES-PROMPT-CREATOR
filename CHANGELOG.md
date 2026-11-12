# Changelog

## 4.1.0 — S10 parity and gate-engine hardening (2026-11-12)
- Consolidates editing/post-production and renderer/code engineering under one S10 owner while preserving both capability lanes and intentionally different source slugs.
- Completes the Ed25519 verifier, removes a malformed unused helper and duplicate CLI entrypoint, restores deterministic transitive invalidation results, and exposes non-destructive apply-invalidation in the active CLI.
- Makes the legacy diagnostic evaluator fail closed for TEST_FIXTURE/non-production projects; production release approval remains separate from synthetic test success.
- Aligns artifact-envelope fixtures and manifest path validation with the required `content_path` contract.
- Fresh CI on the resulting PR head and independent review are required; this changelog does not claim runtime/render/media or human approval PASS.

## 4.0.9 — mandatory M00/S14 preflight (2026-11-12)
- Makes S14 an explicit M00-owned preflight before conversation audits, versioned changes, source reconciliation, GitHub publication and release decisions.
- Preserves S01–S13 production ownership and makes S14 cross-cutting rather than a creative stage.
- Documents poster/image-first, audio-first, transcript-first, script-first and hybrid intake; SRT/VTT, audio-post, SOURCE-to-DELIVERY trace and independent S12 QA boundaries.
- Keeps GitHub editing/post-production and private renderer-code-engineering scopes separate pending owner-approved mapping.

## 4.0.8 — cache-safe validator execution (2026-11-12)
- Prevents the package validator from generating its own Python bytecode before cache-artifact scanning.
- Reorders documented local validation so package hygiene runs before tests and disables pytest bytecode/cache generation for reproducible checks.
- Removes the obsolete build/v4-blocked-gate-report.json artifact path; the actual blocked-fixture report is build/v4-release-gate.json.
- Keeps all cache and bytecode rejection controls active for files actually present in the release package.

## 4.0.7 — validator entrypoint import fix (2026-11-12)
- Fixes package-validator module resolution when invoked directly from the scripts directory by adding the repository root to sys.path before importing the release validator.
- Records the V4.0.6 CI failure and requires fresh CI on the corrected head.
- Keeps the 15 numbered GitHub modules distinct from the private package-only executable-gate-engine helper.

## 4.0.6 — exact skill inventory and validator correction (2026-11-12)
- Corrects the numbered-module inventory and records the private package's additional executable-gate-engine operational helper as an intentional package-only divergence.
- Removes ambiguous skill-count wording and documents that the helper is not S15.
- Corrects SemVer, frontmatter and changelog checks to avoid escaped-regex false failures in the release validator.
- Keeps runtime, Remotion/media QA, license/rights and human approvals separate; production release remains HOLD.

## 4.0.5 — S14 handoff and package hygiene (2026-11-12)
- Clarifies S14 as a cross-cutting preflight for conversation context, release changes and publication evidence.
- Adds an explicit M00 ↔ S14 handoff contract and documents the available-history coverage boundary.
- Aligns root/Codex manifests and enforces the 30-character shortDescription limit.
- Strengthens release validation for duplicate JSON keys across the package, 15-skill inventory, manifest parity and cache/bytecode exclusion.
- Adds .gitignore and publication hygiene checks; known cache paths are excluded from release packages.
- Keeps main CI, independent review, live host, Remotion/media QA, license/rights and human approvals separate; production release remains HOLD.

## 4.0.4 — conversation context and release-integrity controls (2026-11-12)
- Added S14 conversation context/release-change audit to protect requirements and preferences distributed across project conversations.
- Added explicit, confirmed preference, inferred, proposed, unknown and superseded classifications with source-to-release traceability.
- Added strict release consistency checks for duplicate JSON keys, root/Codex manifest parity, README release title and changelog version.
- Reconciled stale repository state: PR #7 is merged; PR-head CI and merge-commit evidence are distinguished.
- Kept runtime, Remotion rendering, artifact QA, rights and human approvals fail-closed; production release remains HOLD.

## 4.0.0 — executable validator and gate-engine implementation
- Introduced strict V4 project, claim, scene, capability and artifact contracts.
- Added executable semantic validation, 21 active deterministic controls and G0–G7 fail-closed transition gates.
- Added source provenance, hash-bound approval structures, dependency invalidation and security/resource policies.
- Added synthetic fixtures, mutation tests, CLI and CI evidence reports.
- Kept 1,000 candidates separate from implemented/executed controls.

## 2.0.0
- Extended poster-first, audio-first, hybrid and script-first workflows; expanded audio intelligence, transcript provenance, SRT/VTT and renderer handoff.

## 1.2.2
- Removed fixed-version assumptions and strengthened semantic-version checks.

## 1.2.0
- Added strict frontmatter parsing, references, manifests and requirement/test/owner/dependency/output traceability.

## 1.0.0
- Initial modular production workflow M00 + S01–S13.
