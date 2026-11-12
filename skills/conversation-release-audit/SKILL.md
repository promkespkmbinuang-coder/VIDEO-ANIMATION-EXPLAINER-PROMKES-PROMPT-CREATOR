---
name: conversation-release-audit
description: "Use before updating, extending, auditing or publishing Video Explainer Promkes releases when requirements, preferences, decisions or blockers are distributed across current and prior project conversations."
---

# S14 — Conversation Context & Release-Change Auditor

## Mission
Protect requirement continuity across conversations and releases. Convert only the conversation history, prior summaries, supplied files, GitHub decisions, CI evidence and package state actually available into a traceable context register and change-impact plan. This skill complements M00 and S01–S13; it does not replace clinical review, specialist ownership, independent QA, GitHub review or human release approval.

Conversation context proves only that a request or preference was expressed. It does not prove a health claim, current campaign fact, permission, file presence, identity, external capability or test result. State the coverage boundary; never claim that inaccessible chats/files were audited.

## 1. Context intake and classification
Inspect the current conversation, available prior-conversation summaries, supplied project documents and relevant project files. For each material item assign:
- EXPLICIT — directly requested or decided by the user.
- CONFIRMED_PREFERENCE — repeated or explicitly confirmed and still relevant, but editable.
- INFERRED — plausible interpretation not directly confirmed.
- PROPOSED — recommended by the system, not a user requirement.
- UNKNOWN — unavailable, unresolved, conflicted or not verified.
- SUPERSEDED — replaced by a later decision; retain history and superseding reference.

Record CTX-ID, concise statement, source locator/date when available, scope, confidence, status, downstream effects and confirmation requirement. Never silently promote inference or proposal into requirement.

## 2. Preserve the production use case
Check poster/photo/infographic plus caption, audio/transcript, supplied script and hybrid input modes. Where relevant, compile source/claim ledger, Fact Lock, audience/campaign brief, screenplay/VO, visual continuity, storyboard/shot plan, still-reference prompts, optional video prompts, motion specification, audio/subtitles, manifest, renderer handoff, QA and release status. Use risk-based depth; do not force every output on simple tasks.

Recurring preferences include accessible/down-to-earth language, story-led persuasion, a curiosity-building but truthful hook, non-lecturing tone, useful educational insight, key message and actionable CTA. Treat these as optional editable voice-profile candidates, not mandatory rules.

Polewali Mandar dialect and brand greeting such as “Halo Sola Seha’” require current brief/brand-profile fit and grounded examples. Never invent idioms, stereotypes or demographic assumptions. Do not turn one-off DBD/TBC/fogging campaigns, dates, locations, institutions, statistics or CTAs into global facts. Hooks must not mislead, stigmatize, manipulate fear or strengthen medical claims.

## 3. Project variables remain project variables
Video aspect ratio, resolution, platform, duration, logo safe areas, typography, subtitles, language, voice, renderer, AI video model, frame rate and audio policy must be scoped per project with PROVIDED, CONFIRMED, INFERRED, DEFAULTED, MISSING, CONFLICTED or NOT_APPLICABLE status. A static poster ratio (including 4:5) does not determine video ratio. Hold only a dependent operation when a missing variable materially affects safety, rights, compatibility or correctness; otherwise expose a reversible assumption/placeholder.

## 4. Change trace and parity
Build the trace:
conversation/source → CTX/INT/REQ-ID → owning skill/artifact → CHG-ID → dependency closure → test/AC-ID → evidence → release disposition.

Compare root/Codex manifests, skills, schemas, scripts, docs, examples, binary assets, reports, CI, private Plugin Creator read-back and GitHub main/branch/PR/commit. Mark source items SYNCED, INTENTIONALLY_DIVERGENT, MISSING, STALE, BLOCKED or NOT_CHECKED. Matching version strings do not prove equal source trees.

Historical tests must identify exact package/version/commit/environment. Never carry V3 PASS results forward as V4 evidence. A PR-head CI result is not a main-merge-commit rerun. A synthetic FFmpeg smoke artifact is not a Remotion render or final health video.

## 5. Impact, invalidation and tests
For every accepted change record old/new version, reason, source intent, changed files, affected skills, dependency IDs, migration impact, positive/negative/edge/security/regression tests, evidence, rollback and approval revalidation. Use the V4 non-destructive invalidation workflow to create a new snapshot; do not overwrite source project state. Downstream locks, hash-bound approvals and artifacts may require invalidation and renewed review.

## 6. GitHub and release governance
Publish source changes on an auditable branch and pull request. Strictly validate duplicate JSON keys, manifest parity, version/changelog/README, package structure, Markdown links, pytest and fail-closed fixtures. Record branch, commit, PR, CI run IDs and merge state. Private plugin save/read-back, GitHub commit, CI, host invocation, real renderer, media QA and human approval are separate statuses.

Do not add a license without an explicit rights-holder decision. Repository visibility is not a license. Publishing source does not authorize clinical, legal, rights, institutional or media release.

## 7. Release gates
Report separately: conversation coverage; requirement/context completeness; private package save/read-back; GitHub publication/merge; CI/static tests; live ChatGPT installation/invocation; external AI/ASR/TTS; Remotion dependency install/Studio/bundle/render/media QA; clinical/legal/rights/privacy/brand/accessibility approval; final production release.

NOT_RUN, BLOCKED, NOT_VERIFIED, UNKNOWN, PARTIAL, STALE and INVALIDATED are never PASS. Return PASS, PASS_WITH_LIMITATIONS, HOLD or FAIL with evidence. Production/public release remains HOLD while mandatory external or human gates are open.
