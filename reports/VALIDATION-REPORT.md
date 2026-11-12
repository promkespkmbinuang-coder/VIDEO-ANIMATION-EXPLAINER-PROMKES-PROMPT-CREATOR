# Validation report — V4.1.4 private package overlay

**Date:** 12 November 2026 (Asia/Makassar)

## Evidence and limits
- Private baseline before this overlay: V4.1.3, USER / PRIVATE; release ID `pluginrel_6af5e443fb8c8191a6c52afacb0a05ea`.
- This overlay updates manifests, context-register version/wording, release docs and S14 handoff version. It intentionally leaves the private legacy gate engine unchanged.
- Private full validator and pytest after V4.1.4 overlay: **NOT_RUN** until executed against the read-back package.
- GitHub V4.1.3 candidate head `2b32135e981a738b35cace88f55d3eb61d66175c`: strict package validation PASS; manifest/duplicate-key consistency PASS; pytest **92 passed, 1 failed**. The failing assertion expected the phrase `not guaranteed`, while the source used `not performance guarantees`. V4.1.4 aligns the source wording to the test oracle and requires fresh CI on the new head.
- Existing `reports/test-results.json` is a legacy V3 ledger, not current V4 evidence; see `docs/legacy-v3-test-results-scope.md`.

## Open issues
1. PR #16 remains Draft/review-pending. Current V4.1.4 exact-head CI is required before independent review.
2. Private engine `CTRL-*` and GitHub candidate `V4-CTL-*` remain PARTIAL / NOT_SYNCED.
3. Private Remotion adapter/assets are not reconciled to GitHub. Prior npm dependency installation was blocked by DNS `EAI_AGAIN`; Studio, real package typecheck, bundle, render and MP4 QA NOT_RUN.
4. ChatGPT live invocation, external AI/ASR/diarization/TTS, clinical/legal/rights/privacy/brand/accessibility approval and final release approval NOT_RUN/NOT_VERIFIED.
5. Canonical plugin/repository naming and license decision remain unresolved.

**Disposition: corrective private context/documentation update only; engine parity PARTIAL / NOT_SYNCED; production/public release HOLD.**
