# Validation report — Video Explainer Promkes V4.0.4

**Date:** 2026-11-12 (Asia/Makassar)  
**Overall production disposition:** HOLD

## Verified package and source evidence

- Private Plugin Creator V4.0.4 saved successfully; read-back confirmed 15 primary skill files and no missing or size-limited paths. Current release ID: `pluginrel_6af5b81e2dbc8191a7af92981b59f916`.
- GitHub PR #7 is closed and merged to main at `11e9d0c746d11934eadf8caa50aa12550b8eceaa`.
- CI run `43212943964` (validate-package) and `43212943521` (markdown-link-check) both succeeded on pre-merge PR head `ad8013ccfe4dbfa92a91cd4751cd0c30316bca27`. PR description reports 51 pytest passes on that head. Do not represent this as a fresh run against the merge commit.
- New overlay validator locally: 3 tests passed; conversation-context JSON Schema Draft 2020-12 validity and synthetic instance passed; overlay ZIP integrity passed. These are tests of overlay files, not a rerun of the complete V4 repository suite.

## Runtime and production boundaries

| Area | Status | Evidence / limit |
|---|---|---|
| Private plugin source save/read-back | PASS | V4.0.4, 15 primary skills; not host installation. |
| GitHub PR #7 merge | PASS | Merge commit listed above. |
| PR-head CI | PASS | Two workflows succeeded; head SHA differs from merge commit. |
| New release consistency overlay | PASS | 3/3 local tests plus schema and ZIP checks. New GitHub PR CI is pending. |
| ChatGPT host | NOT_INSTALLED / NOT_RUN | Current Plugin Management reports not_installed; no live invocation. |
| Remotion dependencies | BLOCKED at last observation | npm registry EAI_AGAIN in prior compatibility run. |
| Remotion Studio/typecheck/bundle/render/MP4 QA | NOT_RUN | No real Remotion packages or output evidence. |
| FFmpeg smoke | LEGACY SEPARATE SMOKE | Not a Remotion render or final Promkes video. |
| External AI video model | NOT_SELECTED | Runtime NOT_RUN. |
| Human clinical/legal/rights/privacy/brand/accessibility approval | NOT_VERIFIED / NOT_RUN | No authorized records inspected. |
| GitHub/private source-tree parity | NOT_RECONCILED | Remotion adapter/assets and some code/schema differences remain. |
| License | UNKNOWN / HOLD | No explicit rights-holder decision; none added. |

The former V3.0.x AT-001..AT-033 / 31-test report is legacy evidence, not a V4.0.4 test result. The 1,000 candidate controls are definitions, not 1,000 executed tests.

## Remaining release blockers

1. Install and invoke the private plugin in the real ChatGPT host with a harmless M00/S14 test.
2. Install pinned Remotion/React packages; run real declaration typecheck, Studio discovery, bundle and render.
3. Decode and inspect actual Remotion video/audio/subtitle artifacts.
4. Select and test an external video model only if the project requires one.
5. Obtain hash-bound authorized clinical, legal/privacy/rights, brand, accessibility and final publisher approvals.
6. Reconcile the full GitHub/private source trees file-by-file; the Remotion adapter and sample assets are not yet in GitHub.
7. Decide license terms with the rights holder before claiming open-source or redistribution rights.

**Disposition remains HOLD.** Passing package/static tests or publishing code does not open external or human release gates.
