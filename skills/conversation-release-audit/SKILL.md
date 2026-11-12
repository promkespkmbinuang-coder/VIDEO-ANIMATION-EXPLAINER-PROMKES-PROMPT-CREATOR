---
name: conversation-release-audit
description: "Use before updating, extending, auditing or publishing Video Explainer Promkes releases when requirements, preferences, decisions or blockers are distributed across current and prior project conversations."
---

# S14 — Conversation Context & Release-Change Auditor

## Mission and boundaries

Protect requirement continuity across conversations and releases. Convert only the current conversation, available prior-conversation summaries, supplied documents, GitHub decisions, validated test records and package read-back actually available into a traceable context register and change-impact plan. State the coverage boundary; never claim that inaccessible raw chats or files were audited.

Conversation context proves that a request or preference was expressed. It does not prove clinical truth, current campaign facts, permissions, asset presence, identity, external capability or test success. S14 does not replace S02 clinical evidence review, S12 independent QA, GitHub review or human release approval.

## 1. Context classification

Classify each material item as EXPLICIT, CONFIRMED_PREFERENCE, INFERRED, PROPOSED, UNKNOWN or SUPERSEDED. Record CTX-ID, exact statement, source locator/date, scope, confidence, status, downstream refs and confirmation requirement. Never silently promote inference or proposal into a requirement.

## 2. Preserve the Promkes production use case

Check poster/photo/infographic plus caption, audio/transcript, supplied script and hybrid inputs. Where relevant, compile source/claim ledger, Fact Lock, audience/campaign brief, screenplay/VO, visual/continuity guides, storyboard/shot plan, still-reference prompts, optional video prompts, motion specification, audio/subtitles, manifest, renderer handoff, QA and release status. Use risk-based depth; do not force every deliverable on a simple request.

Recurring optional voice-profile candidates include accessible/down-to-earth Indonesian, story-led persuasion, a curiosity-building but truthful hook, non-lecturing tone, useful educational insight, key message and actionable CTA. Polewali Mandar dialect and “Halo Sola Seha’” require current brief/brand-profile fit and grounded examples. Never invent idioms, stereotypes or demographic assumptions.

Do not globalize one-off DBD/TBC/fogging campaigns, dates, locations, institutions, statistics or CTAs. A static poster's 4:5 ratio/logo-safe margin does not determine video ratio. Hooks must not mislead, stigmatize, manipulate fear or strengthen medical claims.

## 3. Project variables

Video aspect ratio, resolution, platform, duration, logo safe areas, typography, subtitles, language, voice, renderer, AI video model, frame rate and audio policy are project variables. Label each PROVIDED, CONFIRMED, INFERRED, DEFAULTED, MISSING, CONFLICTED or NOT_APPLICABLE. Hold only dependent operations when missing data materially affects safety, rights, compatibility or correctness; otherwise expose reversible assumptions.

## 4. Trace and change impact

Build: conversation/source → CTX/INT/REQ-ID → owning skill/artifact → CHG-ID → dependency closure → test/AC-ID → evidence → release disposition.

For each accepted change record old/new version, reason, source intent, affected files/skills, dependency IDs, migration impact, positive/negative/edge/security/regression tests, evidence, rollback and approval revalidation. Preserve superseded records; do not overwrite source project snapshots. Revalidate dependent artifacts and renew hash-bound approvals when necessary.

## 5. Release parity and publication

Compare root/Codex manifests, skills, schemas, scripts, docs, examples, binary assets, reports, CI, private Plugin Creator read-back and GitHub main/branch/PR/commit. Mark each component SYNCED, INTENTIONALLY_DIVERGENT, MISSING, STALE, BLOCKED or NOT_CHECKED. Matching version strings do not prove source-tree parity.

Publish source changes on an auditable branch and pull request. Strictly validate duplicate JSON keys, manifest parity, version/changelog/README, skill inventory, package hygiene, Markdown links, pytest and fail-closed fixtures. Record branch, commit, PR, CI run IDs and merge state. A PR-head CI result is not a post-merge main CI result.

Do not add a license without an explicit rights-holder decision. Repository visibility is not a license. Source publication does not authorize clinical, legal, rights, institutional or media release.

## 6. M00 handoff contract

For version audit, package update, GitHub publication or release-readiness work, S14 is a mandatory preflight before M00 changes versioned artifacts. Hand off coverage boundary, context register, confirmed requirements/preferences versus inference/proposal/unknown, superseded decisions, source-to-requirement-to-artifact trace, changed files/dependency closure, tests/evidence to rerun, and release blockers.

M00 retains orchestration and gate arbitration. S14 does not decide clinical truth, creative ownership, human authority or independent QA. If S14 is unavailable, mark the preflight NOT_RUN; do not imply it occurred.

## 7. Release status

Report separately: conversation coverage; requirement/context completeness; private package save/read-back; GitHub source publication/merge; CI/static tests; live ChatGPT installation/invocation; external AI/ASR/TTS; Remotion install/Studio/bundle/render/media QA; clinical/legal/rights/privacy/brand/accessibility approval; final production release.

NOT_RUN, BLOCKED, NOT_VERIFIED, UNKNOWN, PARTIAL, STALE and INVALIDATED are never PASS. Production/public release remains HOLD while mandatory external or human gates are open.
