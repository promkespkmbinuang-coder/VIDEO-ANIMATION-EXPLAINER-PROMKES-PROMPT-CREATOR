# Engine source parity — GitHub source candidate

**Audit date:** 2026-11-12 (Asia/Makassar).

## Private Plugin Creator V4.1.1

- Plugin ID: `plugins_6af57525bfdc8191af0a262699b6df58`
- Release ID: `pluginrel_6af5d06d0c388191840a4861eadd953c`, scope USER, discoverability PRIVATE.
- `scripts/v4_gate_engine.py`: 47,607 characters / 849 lines.
- Verified markers: legacy `CTRL-*` registry present; `V4-CTL-*` absent; Ed25519 / `verify_approval_signature` absent; one `main()`; `evaluate_project()` and `apply_invalidation()` present.
- The legacy evaluator does not enforce the new `project_mode == PRODUCTION` synthetic-fixture guard. Its `release_eligible` output is not production authorization. The executable-gate-engine skill now explicitly prohibits using it as release approval.

## GitHub PR #14 candidate

- PR: https://github.com/promkespkmbinuang-coder/VIDEO-ANIMATION-EXPLAINER-PROMKES-PROMPT-CREATOR/pull/14
- Head at audit before this parity-note commit: `78b294e6901a87dd15a31a9ef1fa54a45590389c`; base main `6aa128ebaa8d561fcedf7a52f027bd2a2a931198`.
- Candidate engine contains `V4-CTL-*`, completed Ed25519 verifier path, deterministic invalidation, non-destructive `apply-invalidation`, stricter path guard and synthetic-fixture production release blocking.
- Validate-package #225 (ID `43239540057`) and markdown-link-check #229 (ID `43239539607`) SUCCESS on that exact PR head.
- PR #14 remains OPEN + DRAFT, no independent review recorded, and is not merged into main.

## Required sequence

1. Independent reviewer audits PR #14 engine, trust semantics, schemas, tests and CLI.
2. Resolve review findings; keep latest-head CI green.
3. Merge only after authorized human approval; verify merge commit and post-merge main CI on exact SHA.
4. Synchronize reviewed engine, schemas, tests, docs and control maps into private plugin using a current-release guard.
5. Run private-package validator/full tests; read back release ID and compare file hashes.
6. Mark engine parity SYNCED only after all above. Until then: `PARTIAL / NOT_SYNCED`.

A green PR run is not private-plugin engine validation. Neither implementation establishes human identity/authority, clinical/legal rights approval, live AI/ASR/TTS, Remotion runtime/render, MP4 QA or final release approval.
