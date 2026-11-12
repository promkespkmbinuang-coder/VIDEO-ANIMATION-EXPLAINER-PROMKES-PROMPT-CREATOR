# Engine source parity — V4.1.2 audit snapshot

**Status: PARTIAL / NOT_SYNCED.** Private Plugin Creator and GitHub PR candidate are two different executable engines. Shared version numbering is not evidence of source/runtime parity.

## Private Plugin Creator V4.1.1
- Release ID: `pluginrel_6af5d06d0c388191840a4861eadd953c`, scope USER, discoverability PRIVATE.
- `scripts/v4_gate_engine.py`: 47,607 characters / 849 lines, `ENGINE_VERSION=4.0.0`, legacy `CTRL-*` control registry, one `main()`, no duplicate top-level definitions.
- No `V4-CTL-*`, Ed25519 verifier or explicit TEST_FIXTURE production guard. Legacy release eligibility is diagnostic only, not production authorization.

## GitHub PR #14 candidate
- Base main: `6aa128ebaa8d561fcedf7a52f027bd2a2a931198`.
- Previous exact validated head: `17bbee4c217c11056a07bc009682c3c55c3a7cf5` (validate-package and link-check SUCCESS); current V4.1.2 head needs fresh CI.
- Candidate engine includes `V4-CTL-*`, Ed25519 verification, deterministic dependency invalidation, non-destructive `apply-invalidation`, stricter path guard and TEST_FIXTURE release blocking.
- Candidate changes are not merged or synchronized to the private package.

## Safe synchronization
1. Independent review of engine semantics, schemas, control registry, approval model and CLI.
2. Resolve review findings and require green CI on exact latest PR head.
3. Merge only after authorized approval; verify merge commit and direct main CI.
4. Synchronize engine, schemas, fixtures, tests, controls and docs with the guarded private release update.
5. Run private validator/full tests, read back release and compare paths/hashes/behavior.
6. Declare SYNCED only after all above; otherwise retain PARTIAL / NOT_SYNCED.

Ed25519 proves a signature against a supplied trust map; it does not establish identity/authority without an independently protected institutional trust registry. Runtime/media/clinical/rights/human approval gates are separate.
