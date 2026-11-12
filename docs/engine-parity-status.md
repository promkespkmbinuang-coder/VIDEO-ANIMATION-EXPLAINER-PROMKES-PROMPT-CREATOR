# Engine source parity — V4.1.3 audit snapshot

**Status: PARTIAL / NOT_SYNCED.** Private Plugin Creator and GitHub PR candidate are different executable engines. Shared release numbering is not evidence of source/runtime parity.

## Private Plugin Creator V4.1.3
- Package release: `pluginrel_6af5d45a51f8819186ace7bdaea5e51d` was the V4.1.2 baseline; V4.1.3 overlay release/read-back is pending.
- Engine remains legacy `CTRL-*` (engine core unchanged from prior package), not the GitHub candidate registry.
- No V4-CTL candidate, verified Ed25519 trust chain or explicit TEST_FIXTURE production guard was merged into this private update. Legacy `release_eligible` is diagnostic, not production authorization.

## GitHub PR #14 candidate at audit intake
- Branch `release/v4.0.5-package-hygiene-s14`; previously checked head `b92eb75e8be09c86e4dbd7f391a7913da163ba9e`.
- At that exact head: validate-package run `43241911591` SUCCESS (93 passed in 1.49s); markdown-link-check run `43241911577` SUCCESS.
- PR #14 was OPEN + DRAFT, unmerged, with no independent review submission or review thread at audit intake.
- V4.1.3 branch changes require fresh CI on the new exact SHA; previous-head evidence does not carry forward.

## Safe synchronization
1. Independent review of engine semantics, schemas, control registry, approval model, trust-root provenance and CLI.
2. Resolve review findings and require green CI on exact latest PR head.
3. Merge only after authorized approval; verify merge SHA and direct main CI.
4. Synchronize engine, schemas, fixtures, tests, control map and docs together in a guarded private release.
5. Run private validator/full tests, read back release and compare files/hashes/behavior.
6. Declare SYNCED only after all above; otherwise retain PARTIAL / NOT_SYNCED.

A valid Ed25519 signature against a supplied trust map does not by itself establish the real-world identity or authority of the signer. Runtime, media, rights and human approvals are separate gates.
