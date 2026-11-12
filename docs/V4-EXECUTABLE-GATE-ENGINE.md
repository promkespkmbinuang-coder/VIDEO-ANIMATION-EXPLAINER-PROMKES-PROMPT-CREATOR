# M00 V4 — Executable Validator and Gate Engine

**Engine:** `promkes-v4-gate-engine` · **Version:** `0.1.0` · **Python:** 3.11+

## Executable scope

The core implements 21 deterministic controls across G0–G7. The active registry is `schemas/v4/control-registry.v4.json`; executable adapters are in `scripts/v4_gate_engine.py`. Each active control has a positive-path test on a synthetic fixture and a negative/mutation test. The gate-fail-closed test fault-injects a deliberately broken evaluator and confirms that a permissive regression is detected.

Implemented checks: strict JSON duplicate-key rejection; JSON Schema Draft 2020-12; canonical JSON and SHA-256; source/claim provenance; unverified-claim fail-closed rules; clinician review; unique IDs; contiguous frame timeline; dependency DAG and transitive invalidation; path traversal/symlink defenses; artifact content hashes; exact renderer capability/version/expiry; privacy, rights and resource limits; prompt/source instruction boundary; Ed25519 role-bound approval signatures over hash-bound payloads; control evidence digests; ordered G0–G7 gates.

## Reproducible commands

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/validate_package.py
python scripts/v4_gate_engine.py validate examples/v4/smoke-project.json --schema-dir schemas/v4
python scripts/v4_gate_engine.py run-controls examples/v4/smoke-project.json --report build/v4-controls.json --updated-project build/v4-evidenced-project.json
python scripts/v4_gate_engine.py gate build/v4-evidenced-project.json --target G6_CODE_VALID --report build/v4-pre-release-gates.json
```

To examine the final release guard, execute `gate --target G7_RELEASE_APPROVED` against the smoke fixture. Exit code 2 and `BLOCKED` are intentional: the fixture declares `project_mode=TEST_FIXTURE`, which must never be publishable. CI asserts that block as a positive safety test.

## Gate semantics

Each downstream state requires every predecessor to be PASS. A required control must be PASS with complete, valid, untampered execution metadata, current engine version, matching subject hash and a valid evidence digest. NOT_RUN, NOT_VERIFIED, BLOCKED, STALE, INVALIDATED, FAIL and PARTIAL never become PASS. The initial active registry has explicit controls; NOT_APPLICABLE is not an implicit skip.

G7 additionally rejects test fixtures and requires artifact QA tied to a content-hash-verified artifact plus an Ed25519-signed, authorized RELEASE_APPROVER decision tied to that hash.

## Approval trust

Ed25519 verifies signatures over a canonical payload with role, identity, decision, artifact hashes, scope, key ID and time fields. The trusted key registry and authorized approver roster must be issued and maintained by the institution outside the project. The `authority_verified` flag is an attestation, not identity proof. Key revocation, signer competency and chain-of-authority remain external trust-root responsibilities.

## Scope boundaries

The smoke project is synthetic; its test keys and mock renderer capability are not production credentials and must never be reused in a real project. CI PASS proves deterministic software behavior against these inputs, not clinical correctness, identity, institutional authority, external source authenticity, rights clearance, real renderer availability, actual MP4 creation, perceptual media QA, accessibility user testing or publication approval.

The evidence digest is tamper-evident but not an authenticated timestamp. Source and capability statuses are structurally validated; this engine does not browse sources or probe external providers. Prompt firewall checks asserted data-boundary metadata and tested negative cases; it is not a universal injection detector. The engine does not execute renderer code, ASR, diarization, TTS or media processing.

The 10×10×10 model enumerates 1,000 candidate definitions, not 1,000 executable controls. Only the explicit 21-control registry is active and tested; further controls require objective, applicability, oracle, evidence contract, owner, remediation and reproducible tests.
