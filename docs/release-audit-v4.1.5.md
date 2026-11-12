# Release audit — V4.1.5

**Date:** 13 November 2026 (Asia/Makassar). **Disposition:** source/audit update; production/public media release **HOLD**.  
**Conversation coverage:** PARTIAL_WITH_DISCLOSED_BOUNDARY. Current turn, available prior summaries, selected private Plugin Creator read-backs, GitHub repository/PR/CI metadata and acceptance specifications were reviewed. Complete raw historical chats and all earlier project artifacts were unavailable.

## Version and repository baseline
The user-facing plugin link label still contains a V4.0.3 alias, but backend plugin ID `plugins_6af57525bfdc8191af0a262699b6df58` currently resolves to private USER/PRIVATE V4.1.4, release `pluginrel_6af5e73b7bb88191909f75be1cd0de41`. Read-back: 100 files, no missing/size-limited paths. V4.0.3 is historical, not current. GitHub main is V4.1.4 at `8330b9e61eb37c94d38630188dce3a75721d1643`.

## GitHub state reconciled
- PR #14 is MERGED at `0e9c56a0246852d3a36bf1b28b8bb5078cb8bd11`; prior OPEN/DRAFT text is stale.
- PR #16 is MERGED at `8330b9e61eb37c94d38630188dce3a75721d1643`; its body still says Draft/review pending, now stale.
- No review submissions returned for PR #14 or #16; PR #16 has no review thread. Merge is not an independent review or institutional authorization.
- Exact main SHA CI:
  - [validate-package run 43258911702](https://github.com/promkespkmbinuang-coder/VIDEO-ANIMATION-EXPLAINER-PROMKES-PROMPT-CREATOR/actions/runs/43258911702): SUCCESS; strict package validation passed; **93 pytest passed in 1.42s**; schema/gate checks completed; synthetic TEST_FIXTURE was correctly kept BLOCKED.
  - [markdown-link-check run 43258911670](https://github.com/promkespkmbinuang-coder/VIDEO-ANIMATION-EXPLAINER-PROMKES-PROMPT-CREATOR/actions/runs/43258911670): SUCCESS.
These apply to that exact GitHub main SHA only, not the private package or live runtime.

## Critical gap — acceptance execution
`tests/acceptance-cases.json` SHA `f8bc26243bdc00c8f399425a22aa0c07f6a3eac6` contains **45 scenario-based acceptance cases; all 45 are NOT_RUN**. They cover source conflicts, unreadable assets, clinical claims, prompt injection, audio/timing, privacy/rights, visual continuity, cross-modal QA, release approval, portability and regression. The 93 pytest checks, active V4 controls and 1,000 candidate-control definitions are separate evidence classes. None closes these 45 cases. The versioned ledger preserves every ID and NOT_RUN state.

## Engine and source parity
GitHub main contains the V4-CTL candidate; private package remains legacy 21-control CTRL. The private legacy `evaluate`/`--require-release` path is diagnostic, not production authorization. Do not claim the GitHub V4-CTL, Ed25519 trust/identity path or TEST_FIXTURE guard exists in the private engine.
Private package contains Remotion/React TSX adapter/assets not evidenced in GitHub main. Path/name matches do not establish byte, behavior or runtime parity. Private plugin name, GitHub root manifest name and repository slug differ; canonical identity remains unresolved.

## Conversation continuity retained
The effective register keeps the prior 26 records and adds CTX-QA-027. It preserves input modes (poster/caption, audio/transcript, script, hybrid); editable accessible Indonesian storytelling; truthful hook, non-preachy style, educational insight, key message and CTA; optional greeting/dialect; 1080×1350 px/4:5/logo-safe margins only for static infographics; superseded 30 Oct 2026 CKG/HKN banner; campaign-scoped DBD/TBC/fogging details; optional social captions/hashtags; no FYP/viral guarantees; unspecified AI provider; and the distinction between adapter code and real Remotion render.

## Gate summary
| Area | Status |
|---|---|
| Exact-main GitHub package validation and pytest 93 | PASS |
| Exact-main Markdown link check | PASS |
| Scenario acceptance suite | NOT_RUN (45/45) |
| Private V4.1.4 full tests | NOT_RUN |
| Private CTRL ↔ GitHub V4-CTL | PARTIAL / NOT_SYNCED |
| ChatGPT install/live invocation | NOT_VERIFIED / NOT_RUN |
| AI provider | NOT_SELECTED / NOT_RUN |
| ASR/diarization/TTS | NOT_RUN |
| Remotion install/Studio/typecheck/bundle/render | BLOCKED or NOT_RUN; last npm registry observation EAI_AGAIN |
| MP4 QA | NOT_RUN |
| Clinical/legal/privacy/rights/brand/accessibility approvals | NOT_VERIFIED / NOT_RUN |
| License / redistribution | UNKNOWN_NOT_ADDED |
| Final human release approval | NOT_VERIFIED |

**Production/public media release remains HOLD.** Passing repository CI does not mean deployment, plugin installation, external generation, media QA or clinical release.
