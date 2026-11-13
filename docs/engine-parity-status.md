# Engine source parity — V4.1.5 audit snapshot

**Status: PARTIAL / NOT_SYNCED.** GitHub and private Plugin Creator packages have different executable gate engines. Release version equality is not engine parity.

## Private Plugin Creator engine
- Baseline private release at audit intake: V4.1.4, `pluginrel_6af5e73b7bb88191909f75be1cd0de41`, USER / PRIVATE.
- Private `scripts/v4_gate_engine.py` remains the legacy 21-control `CTRL-*` engine with structural approval records.
- It does not include GitHub's V4-CTL candidate implementation, trusted institutional Ed25519 identity/authority chain, or the GitHub TEST_FIXTURE production guard.
- Do not use the legacy `evaluate` or `--require-release` result as final production authorization. Treat synthetic, test, demo, mock, incomplete, unsigned or non-production projects as BLOCKED.

## GitHub candidate now in main
- PR #14 is MERGED at `0e9c56a0246852d3a36bf1b28b8bb5078cb8bd11`.
- PR #16 is MERGED at `8330b9e61eb37c94d38630188dce3a75721d1643`.
- Current main SHA: `8330b9e61eb37c94d38630188dce3a75721d1643`.
- Exact-main `validate-package` run [43258911702](https://github.com/promkespkmbinuang-coder/VIDEO-ANIMATION-EXPLAINER-PROMKES-PROMPT-CREATOR/actions/runs/43258911702): SUCCESS, 93 pytest passed, strict package validation passed, and fail-closed V4 gate smoke checks completed.
- Exact-main `markdown-link-check` run [43258911670](https://github.com/promkespkmbinuang-coder/VIDEO-ANIMATION-EXPLAINER-PROMKES-PROMPT-CREATOR/actions/runs/43258911670): SUCCESS.
- No review submissions were returned for PR #14 or #16. CI/merge does not establish independent review or institutional authorization.

## Safe synchronization protocol
1. Obtain independent technical review of the GitHub gate semantics, schema, controls, signature verification, trust-root provenance, fixtures and CLI.
2. Resolve review findings and confirm owner authorization for private engine migration.
3. Pin the exact main commit, schemas, fixtures, test suite and registry.
4. Synchronize the engine and all dependent schemas, tests, fixtures, docs and control maps atomically in a guarded private package update.
5. Run the private package validator and full test suite; read back release ID; compare file hashes and behavior; exercise positive and negative paths.
6. Declare SYNCED only after exact evidence for all prior steps. Otherwise retain PARTIAL / NOT_SYNCED.

A cryptographic signature against a supplied trust map alone does not prove real-world signer identity, clinical competence or delegated institutional authority. Runtime, media, rights and human approvals remain independent gates.


## V4.1.5 PR #18 validation update
- PR #18 is OPEN + DRAFT; current head ad18796b45bc37d433121d3a39cb856489629aad.
- Exact-head validation run [43266406327](https://github.com/promkespkmbinuang-coder/VIDEO-ANIMATION-EXPLAINER-PROMKES-PROMPT-CREATOR/actions/runs/43266406327) succeeded with 95 pytest passing in 2.08s; link check [43266406293](https://github.com/promkespkmbinuang-coder/VIDEO-ANIMATION-EXPLAINER-PROMKES-PROMPT-CREATOR/actions/runs/43266406293) succeeded.
- An earlier attempt failed 1 new test (94 passed) because of a mismatched source-field name; it was corrected in the current head. Report both attempt and correction, not just the green rerun.
- No independent review submissions for #18 were present at this snapshot. This merge CI does not synchronize or validate the private CTRL engine.
