# Changelog

## 4.0.0 — executable validator and gate-engine implementation
- Introduced strict V4 project, claim, scene, capability and artifact contracts.
- Added executable semantic validation, 21 active deterministic controls, evidence digests and G0–G7 fail-closed transition gates.
- Added Ed25519 cryptographic approval checks bound to canonical claim/artifact hashes and role-scoped trusted keys.
- Added transitive dependency invalidation, asset path/content integrity, capability expiry/version checks, rights/privacy/security/resource policies.
- Added deterministic smoke fixtures, positive/negative mutation tests, CLI reproducibility and CI artifact reports.
- Repaired duplicate/malformed root and compatibility manifests discovered in PR #3 CI.
- Kept 1,000 10×10×10 enumerations strictly separate from implemented/executed controls.
- Production runtime, real Remotion/AI/ASR integrations, MP4 QA and institutional sign-off remain separate evidence requirements.

## 2.0.0
- Extended intake to poster-first, audio-first, hybrid and script-first production modes.
- Expanded audio intelligence, transcript provenance, SRT/VTT, renderer handoff and dual-layer QA.
- Preserved M00 + S01–S13 ownership, Health Truth Registry and continuity governance.

## 1.2.2
- Removed a fixed-version assumption from the validator; it now checks semantic-version syntax and manifest parity.

## 1.2.1
- Corrected suite-aware test-schema validation for baseline AT and reference REF cases.

## 1.2.0
- Added strict YAML frontmatter parsing, reference validation, compatibility manifests and requirement/test/owner/dependency/output traceability.

## 1.1.0
- Clarified Prompt-to-Reference boundaries and downstream renderer handoff.

## 1.0.0
- Initial modular release M00 + S01–S13.
