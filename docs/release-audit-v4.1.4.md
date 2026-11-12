# Release audit — V4.1.4

**Date:** 12 November 2026 (Asia/Makassar). **Conversation coverage:** `PARTIAL_WITH_DISCLOSED_BOUNDARY`; current conversation, available prior-conversation summaries and selected private/GitHub read-backs were available, not the complete raw historical corpus.

## Context delta
The context register grows from 19 to 26 records. New explicit items:
- static infographic 1080×1350 px, 4:5 portrait and generous top/bottom logo-safe area, strictly static-artwork scoped;
- social discovery/reach/views/FYP/trending/likes/comments/shares as aspirations, not promises;
- optional metaphor/hyperbole bounded by S02 Fact Lock;
- environmental-care CTA scoped to the earlier DBD/fogging campaign;
- modern/aesthetic/youth-aware visual language as editable style direction, not a demographic inference;
- unresolved canonical private-plugin / GitHub-manifest / repository naming;
- legacy V3 test ledger cannot validate V4.1.4.

Existing continuity remains: poster/caption and audio/script/hybrid input modes; accessible Indonesian storytelling; truthful hooks; key message/CTA; optional greeting/dialect; campaign-specific DBD/TBC/fogging, dates, places, institutions and statistics; Remotion/React TSX target when selected; AI provider deliberately unspecified; GitHub publication intent; past CKG/HKN brief on 30 October 2026 remains SUPERSEDED.

## Critical findings
1. Private Plugin Creator current release before this update: V4.1.3, `pluginrel_6af5d45a51f8819186ace7bdaea5e51d`, USER/PRIVATE.
2. GitHub PR #14 / #15 had merged to main after the prior release audit, unmerged, and had no independent review or review threads at audit intake. Its PR #16 V4.1.3 candidate head `2b32135e981a738b35cace88f55d3eb61d66175c` passed strict package and manifest validation, but pytest ended with 92 passed / 1 assertion mismatch; V4.1.4 corrects the assertion phrase and requires fresh exact-head CI.
3. GitHub root and private Plugin Creator manifests use different plugin names; repo slug is also distinct. Canonical identity requires explicit owner confirmation; no rename is made.
4. Private engine remains legacy `CTRL-*`; GitHub PR #14 engine remains separate V4-CTL candidate. No engine code synchronization is included.
5. `reports/test-results.json` contains V3-era AT records; they are not V4.1.4 evidence. See `docs/legacy-v3-test-results-scope.md`.

## Test truth at package preparation
- Private Plugin Creator full validator/pytest after overlay: `NOT_RUN`.
- New private context-register schema/uniqueness test: `NOT_RUN` until executed on the private package.
- GitHub validation on previous PR head `b92eb75e8be09c86e4dbd7f391a7913da163ba9e`: prior-head success only; current V4.1.4 changes require new exact-head CI.
- Host invocation, external AI/ASR/diarization/TTS, Remotion installation/Studio/bundle/render, MP4 QA, clinical/legal/rights/privacy/brand/accessibility sign-off, license choice and final human release approval remain `NOT_RUN`, `NOT_VERIFIED` or `BLOCKED`.

**Disposition: context/docs/package update only; engine parity PARTIAL / NOT_SYNCED; production/public release HOLD.**
