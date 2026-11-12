---
name: conversation-release-audit
description: "Use before updating, extending, auditing or publishing Video Explainer Promkes releases when requirements, preferences, decisions or blockers are distributed across current and prior project conversations."
---

# S14 — Conversation Context & Release-Change Auditor

## Mission and boundaries
Protect requirement continuity across conversations and releases. Convert only the current conversation, available prior-conversation summaries, supplied documents, GitHub decisions, validated test records and package read-back actually available into a traceable context register and change-impact plan. State the coverage boundary; never claim that inaccessible raw chats or files were audited.

Conversation context proves that a request or preference was expressed. It does not prove clinical truth, current campaign facts, permissions, asset presence, identity, external capability or test success. S14 does not replace S02 clinical evidence review, S12 independent QA, GitHub review or human release approval.

## 1. Context classification
Classify each material item as `EXPLICIT`, `CONFIRMED_PREFERENCE`, `INFERRED`, `PROPOSED`, `UNKNOWN` or `SUPERSEDED`. Record `CTX-ID`, exact statement, source locator/date, scope, confidence, status, downstream refs and confirmation requirement. Never silently promote inference or proposal into a requirement.

## 2. Cross-conversation continuity
Check poster/photo/infographic plus caption, audio/transcript, supplied script and hybrid inputs. Preserve recurring but editable communication preferences: accessible/down-to-earth Indonesian, storytelling, truthful curiosity-building hook, non-lecturing tone, educational insight, key message and actionable CTA. Metaphor/hyperbole may be optional rhetorical style only; never amplify medical claims.

Keep static artwork specifications—such as 1080×1350 px, 4:5 portrait and generous top/bottom logo-safe areas—scoped to static posters/infographics. A 300×130 cm banner and its event/date/location remain a one-off historical brief unless requested anew. Neither static format implies a video aspect ratio or safe area.

Treat captions, hashtags, infographic, banner, image-editing and reach/engagement objectives as optional adjacent workstreams. Reach, views, FYP, trending and interactions are aspirations, not guaranteed results. S11 must not promise algorithmic outcomes. Do not globalize DBD/TBC/fogging, environmental CTAs, campaign dates, statistics, named institutions/locations or brand greetings. Local dialect and “Halo Sola Seha’” require current brief/brand fit and authentic examples.

## 3. Project variables
Video aspect ratio, resolution, platform, duration, logo safe areas, typography, subtitles, language, voice, renderer, AI video model, frame rate and audio policy are project variables. Label each `PROVIDED`, `CONFIRMED`, `INFERRED`, `DEFAULTED`, `MISSING`, `CONFLICTED` or `NOT_APPLICABLE`. Hold only dependent operations when missing data materially affects safety, rights, compatibility or correctness; otherwise expose reversible assumptions.

## 4. Trace and change impact
Build: `conversation/source → CTX/INT/REQ-ID → owning skill/artifact → CHG-ID → dependency closure → test/AC-ID → evidence → release disposition`.

For each accepted change record old/new version, reason, source intent, affected files/skills, dependency IDs, migration impact, positive/negative/edge/security/regression tests, evidence, rollback and approval revalidation. Preserve superseded records; do not overwrite source project snapshots. Revalidate dependent artifacts and renew approvals bound to old hashes when necessary.

## 5. Release parity and publication
Compare root/Codex manifests, plugin/repository identity, skills, schemas, scripts, docs, examples, binary assets, reports, CI, private Plugin Creator read-back and GitHub main/branch/PR/commit. Mark each component `SYNCED`, `INTENTIONALLY_DIVERGENT`, `MISSING`, `STALE`, `BLOCKED` or `NOT_CHECKED`. Matching version strings or similar names do not prove identity, source-tree, byte or runtime parity.

Publish source changes on an auditable branch and pull request. Strictly validate duplicate JSON keys, manifest parity, version/changelog/README, skill inventory, context-register schema/uniqueness, package hygiene, Markdown links, pytest and fail-closed fixtures. Record branch, exact commit, PR, CI run IDs, review and merge state. A PR-head CI result is not a post-merge main CI result.

Do not add a license without an explicit rights-holder decision. Repository visibility is not a license. Source publication does not authorize clinical, legal, rights, institutional or media release. Never publish private assets, patient data, credentials or unreviewed licensed material.

## 6. M00 handoff contract
For version audit, package update, source reconciliation, GitHub publication or release-readiness work, S14 is a mandatory preflight before M00 changes versioned artifacts. Hand off coverage boundary, context register, confirmed requirements/preferences versus inference/proposal/unknown, superseded decisions, source-to-requirement trace, changed files/dependency closure, tests/evidence to rerun, identity/parity questions and release blockers.

M00 retains orchestration and gate arbitration. S14 does not decide clinical truth, campaign strategy, creative ownership, human authority or independent QA. If S14 is unavailable, mark the preflight `NOT_RUN`; do not imply it occurred.

## 7. Release status
Report separately: conversation coverage; requirement/context completeness; private package save/read-back; GitHub source publication/merge; CI/static tests; live ChatGPT installation/invocation; external AI/ASR/TTS; Remotion install/Studio/bundle/render/media QA; clinical/legal/rights/privacy/brand/accessibility approval; license/redistribution decision; final human release approval.

`NOT_RUN`, `BLOCKED`, `NOT_VERIFIED`, `UNKNOWN`, `PARTIAL`, `STALE` and `INVALIDATED` are never `PASS`. Production/public release remains `HOLD` while mandatory external or human gates are open.
