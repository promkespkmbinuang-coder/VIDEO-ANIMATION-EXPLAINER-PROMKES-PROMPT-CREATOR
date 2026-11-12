# Conversation audit and release parity — 2026-11-12

## Scope and confidence

This audit used the current conversation, available prior-conversation summaries, private Plugin Creator V4.0.3 read-back, V4.0.4 read-back after overlay and GitHub main/PR/CI records. Raw full text of every historical conversation was not available. The scope is therefore all available conversation evidence, not exhaustive raw-history retrieval.

## Findings and corrections

| ID | Severity | Finding | Correction |
|---|---|---|---|
| AUD-CTX-001 | High | Requirements/preferences distributed across conversations had no versioned context register. | Added S14, context labels and source-to-release trace chain. |
| AUD-VER-002 | High | Private plugin V4.0.3 while GitHub root/Codex manifests V4.0.0. | Align repository release manifests to candidate V4.0.4; add automated parity validator. |
| AUD-DOC-003 | High | Stale V3 report/31-test records could be read as current V4 evidence. | Publish version-scoped report; V3 tests are legacy, not current V4 evidence. |
| AUD-PR-004 | High | PR #7 prose said OPEN + DRAFT while GitHub state showed closed/merged. | Correct status and distinguish PR-head CI from merge-commit status. |
| AUD-MAN-005 | High | Duplicate JSON keys in GitHub Codex manifest were not rejected by ordinary JSON parsing. | Rebuild both manifests and add strict duplicate-key rejection in CI. |
| AUD-SYNC-006 | High | Private and GitHub source trees differ; Remotion adapter/assets exist in private package but were not found in GitHub main tree. | Mark full source parity NOT_RECONCILED; do not infer it from version parity. |
| AUD-RUNTIME-007 | Critical | ChatGPT plugin not installed/invoked; Remotion dependencies/runtime/render not demonstrated. | Retain NOT_INSTALLED, BLOCKED and NOT_RUN. |
| AUD-APPROVAL-008 | Critical | Clinical/legal/rights/privacy/brand/accessibility/release approvals are not evidenced. | Keep production release HOLD. |
| AUD-LIC-009 | High | Public repository has no explicit license decision. | No LICENSE added; public visibility is not a license. |
| AUD-REQ-010 | Medium | Storytelling, hook, local language and CTA preferences risk becoming hard-coded across campaigns. | Make style an editable project-scoped voice profile; local dialect/greetings remain conditional. |
| AUD-FMT-011 | Medium | Static-poster ratio/logo margins could be misread as video settings. | Keep video ratio/resolution/safe areas project-specific. |

## Conversation-derived intent retained

The available history supports poster/photo/infographic plus caption as the recurring input mode, with audio/transcript, supplied script and hybrid inputs as needed. Relevant outputs can include source/claim ledger, Fact Lock, audience/campaign, screenplay/VO, visual/continuity guides, storyboard/shot plan, still-reference prompts, optional video prompts, motion, audio/subtitles, manifest, renderer handoff, QA and release status. Use proportional depth.

Recurring style preferences include down-to-earth accessible language, story-led persuasion, truthful curiosity-building hooks, a non-lecturing tone, useful educational insight, key message and actionable CTA. Polewali Mandar local flavor and “Halo Sola Seha’” are optional brand-profile values requiring current brief fit and grounded examples. One-off health campaigns, dates, statistics, locations and institutional names are not global facts. A static 4:5 design request does not set video aspect ratio.

## Evidence and limitations

- Private plugin V4.0.3 before update: `pluginrel_6af5a9847a288191af10873f2d72b600`, 14 primary skills, no missing/size-limited paths.
- Private plugin V4.0.4 after update: `pluginrel_6af5b81e2dbc8191a7af92981b59f916`, 15 primary skills, no missing/size-limited paths.
- GitHub PR #7 is merged; merge commit `11e9d0c746d11934eadf8caa50aa12550b8eceaa`.
- PR-head CI #94 succeeded on `ad8013ccfe4dbfa92a91cd4751cd0c30316bca27`: validate-package run `43212943964`; markdown-link-check run `43212943521`. PR description reports 51 tests passed. This is not a direct post-merge run on the merge commit.
- Plugin Management currently reports the private plugin `not_installed`; live invocation NOT_RUN.
- Last Remotion install check was blocked by npm DNS `EAI_AGAIN`; Studio, bundle, actual Remotion render and Remotion MP4 QA NOT_RUN. The prior FFmpeg smoke is separate.
- External AI video provider is NOT_SELECTED.
- Human clinical/legal/rights/privacy/brand/accessibility/release approvals remain NOT_VERIFIED or NOT_RUN.

## Release disposition

**HOLD for production/public release.** GitHub source publication, private Plugin Creator read-back, CI, host invocation, actual renderer, media QA and human approval are separate. Full private/GitHub source-tree parity remains NOT_RECONCILED; the Remotion adapter and companion assets were absent from the inspected GitHub main tree. License decision is unresolved.
