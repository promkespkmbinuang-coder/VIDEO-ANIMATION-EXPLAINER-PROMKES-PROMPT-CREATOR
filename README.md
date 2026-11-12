# Video Explainer Promkes — Evidence-Gated Production System

**Architecture:** M00 + S01–S13 · **Target:** V4.0 · **Release posture:** private plugin / public release HOLD

Sistem produksi explainer animasi promosi kesehatan yang memisahkan klaim faktual, bukti, wording yang diizinkan, narasi, referensi visual, continuity, prompt, scene timing, manifest, renderer capability, QA artefak, aksesibilitas, dan persetujuan manusia. M00 mengoordinasikan spesialis S01–S13 tanpa menganggap spesialis sebagai agen runtime otomatis.

## What V4 adds

- JSON Schema Draft 2020-12 contracts for claim records and artifact envelopes.
- A Python CLI validator and eight sequential fail-closed gates with 21 executable controls.
- Claim-to-source provenance and snapshot hash checks; reviewer-matched, hash-bound approval records.
- Narrative claim traceability and exact safe-wording enforcement.
- Visual continuity/reference locks and untrusted-prompt boundary checks.
- Prompt-injection heuristic scan, frame arithmetic, manifest hash/path validation.
- Exact renderer/provider/version capability checks and evidenced static-code checks.
- Artifact hash checks, accessibility evidence and hash-bound release approval records.
- Dependency DAG validation and transitive invalidation planning.
- Heuristic risk/applicability triage for the 1,000 candidate matrix; no control is auto-excluded or marked executed.
- Reproducible pytest suite and CI evidence artifacts.

## Quick start

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/v4_gate_engine.py --help
python scripts/generate_v4_control_candidates.py --output build/control-candidates.json
python scripts/v4_control_risk_triage.py --input build/control-candidates.json --output build/control-risk-triage.json
python scripts/v4_gate_engine.py validate-claim --input claim.json
python scripts/v4_gate_engine.py validate-artifact --input artifact-envelope.json
python scripts/v4_gate_engine.py evaluate --project project.json --output build/gate-report.json
python scripts/v4_gate_engine.py evaluate --project project.json --require-release
python scripts/v4_gate_engine.py invalidation-plan --project project.json --changed SRC-001
```

See [implementation and validation guide](docs/M00-V4.0-IMPLEMENTATION-AND-VALIDATION.md) and [architecture specification](docs/M00-V4.0-EVIDENCE-CONTRACT-GATED-PRODUCTION-COMPILER.md).

## Gate map

| Gate | Control boundary |
|---|---|
| G0 Intake | Input inventory, privacy, rights basis, byte-verifiable untrusted input |
| G1 Fact Lock | Claim schema/semantics, source provenance, evidence state, clinical reviewer approval |
| G2 Narrative | Claim-ID traceability and exact approved wording |
| G3 Visual | Canon lock and scene reference resolution |
| G4 Prompt | Instruction injection heuristics and trusted/untrusted boundary |
| G5 Manifest | Contiguous frame arithmetic, canonical hash and safe paths |
| G6 Code | Exact renderer capability record and evidenced static checks |
| G7 Release | Local artifact hash, accessibility QA evidence and release approval |

A downstream gate can pass only if every predecessor gate passes. NOT_RUN, NOT_VERIFIED, PARTIAL, BLOCKED, STALE and INVALIDATED are never promoted to PASS. NOT_APPLICABLE requires an explicit rationale.

## Control model: 1,000 candidates ≠ 1,000 tests

The generator enumerates 1,000 candidate IDs (10 domains × 10 gates × 10 test families). Enumeration does not execute controls. The executable implementation currently contains 21 named controls with deterministic tests. Future candidates need their own applicability decision, oracle, positive and negative test, evidence format, remediation and retest rule.

## Integrity and limitations

A PASS means only that a deterministic oracle accepted the supplied data/evidence. SHA-256 establishes byte identity, not factual truth, authority, licence or approval. Structural approval records do not authenticate a person's identity, credentials or cryptographic signature. Prompt scanning is heuristic. The engine checks local artifacts and supplied QA evidence; it does not decode or perceptually inspect MP4. Capability records do not execute Remotion. Live ChatGPT invocation, external AI/ASR/diarization, TTS, actual renderer integration/render, codec and media QA, accessibility user testing, institutional clinical/legal/privacy approvals and final human release decision remain separate.

## Repository status

PR #3 has been merged. Its first post-merge validation run revealed malformed plugin manifests. A follow-up corrective change is being prepared; CI must pass on the actual current head before describing this repository state as green. Public release remains HOLD. Repository visibility alone does not grant an open-source licence; publisher rights and licence decisions remain pending.

Private ChatGPT plugin: https://chatgpt.com/plugins/plugins_6af57525bfdc8191af0a262699b6df58
