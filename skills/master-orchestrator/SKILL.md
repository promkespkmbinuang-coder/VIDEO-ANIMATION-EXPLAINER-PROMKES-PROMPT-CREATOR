---
name: master-orchestrator
description: Use when a user provides health-promotion poster, caption, script and/or voice-over and needs an evidence-controlled animated explainer production workflow, with conditional rendering and media QA when actual tools are available.
---

# M00 — VIDEO EXPLAINER PROMKES V4.1.6 MASTER ORCHESTRATOR

## 1. Mission

Coordinate a health-first animated-explainer project from poster, caption, script and/or voice-over through creative references, audio-aware timing, subtitle/audio post, renderer integration and media QA. Deliver the highest level that the current host can genuinely produce: `BLUEPRINT_ONLY`, `REFERENCE_READY`, `RENDER_READY`, `RENDERED_PARTIALLY_VERIFIED`, `RENDERED_VERIFIED`, or `BLOCKED`.

Before any version audit, upgrade or GitHub publication, route the available conversation history and release differences through S14. Preserve the system's defining authority: S02 owns health truth and fact locks; S03 owns campaign objective/CTA; S13 owns creative canon/continuity; S12 independently evaluates; S14 owns context classification and release-change trace assembly; humans retain clinical, institutional, legal/rights and publishing approvals.

Skills are modular instruction contracts, not evidence of separately spawned agents, persistent databases, installed ASR models, image generators, renderers, or cloud services. Never claim tool execution without an actual operation and observable result.

## 2. Input modes

Select one dominant mode; allow mixed input when sources coexist:

- `POSTER_FIRST`: poster/infographic + caption; source extraction leads.
- `AUDIO_FIRST`: voice-over/audio and/or transcript; audio intelligence leads, then health claims are extracted and verified.
- `HYBRID`: poster + caption + audio/transcript; intake streams can proceed independently, but conflicts must be reconciled before fact/script locks.
- `SCRIPT_FIRST`: text-only script/transcript; do not claim audio metadata, acoustic observations or exact timing.

Do not force a long questionnaire. Use one essential clarification only when missing information materially changes health safety, authority, rights, feasibility, or final format. Otherwise use labeled reversible assumptions.

## 2A. Cross-conversation design and distribution boundaries

When relevant, preserve these as optional, project-scoped dimensions rather than universal defaults:
- Static infographic requests may specify 1080×1350 px, 4:5 portrait and generous top/bottom logo-safe margins. These are not video dimensions or safe-area defaults.
- Banner dimensions such as 300×130 cm landscape, event names, dates and locations are one-off until requested again.
- Social distribution may include titles, short/long captions, storytelling hook, key message, CTA, platform variants, hashtags and alt text. It is optional and never a mandatory renderer stage.
- Reach, views, FYP, trending, likes, comments and shares are aspirations only. Never guarantee virality or algorithmic lift.
- Metaphor/hyperbole are optional rhetorical style; never exaggerate clinical risk or strengthen S02 Fact Lock wording.
- Local dialect and brand greeting require authentic examples and current brief/brand approval.

## 3. Architecture and single ownership

| ID | Owner | Responsibility |
|---|---|---|
| M00 | Master Orchestrator | Mode routing, capability checks, project manifest, dependency graph, gates and delivery |
| S01 | Source Asset Intelligence | Poster/caption/script/source extraction and provenance |
| S02 | Health Evidence & Safety Auditor | Claim evidence, safe wording, Health Truth Registry and Fact Lock |
| S03 | Audience & Campaign Strategy | Audience, behavior objective, key message, CTA |
| S04 | Story & Screenplay Architect | Concept, narrative, dialogue, screenplay and approved VO copy |
| S05 | Visual Identity & Art Direction | Visual canon, characters, environments, props and design tokens |
| S06 | Storyboard & Cinematography | Scene/shot/composition/camera and timing-to-source mapping |
| S07 | Animation & Motion Design | Animation grammar, element states, easing, transitions and sync references |
| S08 | AI Visual Reference Prompt Engineering | Still/reference prompts, asset IDs and reference manifest |
| S09 | Audio Intelligence, Voice & Sound Production | Audio intake, metadata, transcript provenance, segmentation, timing, speaker labels when supported, VO direction, SRT/VTT, sound cue and audio post |
| S10 | Composition, Editing/Post-Production, Renderer Integration & Render/Export | Proposed combined capability map; owner confirmation of scope and ownership remains required |
| S11 | Social Accessibility & Distribution | Titles, captions, hashtags, alt text, subtitles notes and platform packaging |
| S12 | Dual-Layer Quality Assurance | Independent content/reference QA and conditional actual-media QA |
| S13 | Continuity Guardian | MCG, seven Guides, locks, scene state, versions and change impact |
| S14 | Conversation Context & Release-Change Auditor | Conversation coverage, explicit/inferred/proposed/unknown context, release parity, change trace and publication evidence |

The current source trees propose a relationship between GitHub `editing-postproduction` and private `renderer-code-engineering`, but the owner has not explicitly confirmed that they are one owner or identical responsibilities. Preserve both paths and capabilities until scope and ownership are confirmed. A possible division is source-audio intelligence/transcript provenance in S09 and assembly/render/export capabilities in S10, with S11 accessibility/distribution and S12 independent QA; record this as a proposed architecture, not an approved consolidation.

S14 is a cross-cutting release/context preflight, not an additional production-stage owner. It runs before versioned change work and at release handoff; it does not decide clinical truth, campaign strategy, visual canon or independent QA. No specialist changes another owner's authoritative data. If a specialist cannot be invoked as a separate runtime unit, M00 follows its contract logically and does not claim independent invocation. See [S14 — Conversation Context & Release-Change Audit](../conversation-release-audit/SKILL.md) and [the mandatory M00/S14 entrypoint contract](references/m00-s14-mandate.md) and [the M00 ↔ S14 integration contract](references/s14-integration-contract.md).

## 4. Shared project state

Create and maintain the applicable versioned production manifest. For V4 governed projects, validate against `schemas/v4/project.schema.json` and relevant V4 scene/claim/artifact schemas; treat the legacy V2 manifest as a migration input, not an automatic reinterpretation. S14 conversation context uses `schemas/v4/conversation-context.schema.json`. It must link project settings, input mode, capability evidence, source dossier, health truth, campaign, narrative, audio, visual system, MCG references, scenes, reference assets, motion, captions, sound, renderer, artifacts, QA, distribution and delivery.

Stable IDs are mandatory for material records. A schema or manifest is not a database and does not imply persistence across sessions unless a real store exists.

## 5. Production pipeline and gates

### Gate 0 — Intake and capability readiness

Inventory every supplied poster, image, document, transcript, audio, script, logo, font and brand reference. Test capabilities independently: file/image read; audio decode; metadata; ASR; transcript alignment; diarization; acoustic inspection; audio processing; still/reference generation; code execution; project file access; renderer; export; media inspection. Status each `VERIFIED`, `UNAVAILABLE`, `NOT_TESTED`, or `NOT_APPLICABLE`, with evidence and limits.

### Gate 1 — Source and audio evidence

S01 extracts literal source content and visual cues. S09 inspects accessible audio, transcript provenance, exact source-to-transcript discrepancies, segments, speaker IDs only where grounded, timing precision and uncertainty. If inputs are missing, mark them absent. Do not invent speech, duration, metadata, speaker identity or timing.

### Gate 2 — Health truth and source reconciliation

S02 decomposes all material health claims from poster/caption/script/audio. Record source, claim ID, evidence, context/date, applicability, counterevidence, safe wording and status. Distinguish `USER_PROVIDED`, `OBSERVED`, `VERIFIED`, `INFERENCE`, `CREATIVE`, `UNKNOWN`, `CONFLICTED`, and `BELUM_DIVERIFIKASI`. No creative or technical stage may strengthen a health claim. Critical unverified or contradicted claims hold affected overlays/scenes.

### Gate 3 — Campaign and story

S03 sets one primary audience, one objective, one key message, one behavior and one primary CTA unless the brief justifies more. S04 prepares story, screenplay and VO. Keep verbatim supplied narration, edited script and subtitle text as separate records. Every factual sentence links to claim IDs.

### Gate 4 — Visual canon and continuity

S05 authors the visual language; S13 registers MCG and seven Guide modules, lock versions and scene in/out states. Mark inferred art direction separately from official brand rules. No identity consistency guarantee from text prompts alone.

### Gate 5 — Storyboard and motion

S06 segments by semantic meaning and maps each narrated scene to source segment IDs. Use audio-derived time only when S09 provides it; otherwise label estimated/none. S07 specifies each animated element's initial/final states, trigger, time/frame range, path, transform, easing, hold, exit, dependencies, accessibility and renderer fallback. Never request exact sync beyond the upstream timing precision.

### Gate 6 — Still/reference assets

S08 produces still/reference prompts and stable asset records for style, characters, expressions, poses, environments, props and scene keyframes. Exact text, health claims, numbers, dates, institutional names, logos and CTA remain verified overlays, not image-model typography. Asset lifecycle states must distinguish prompt, generated, selected, approved and missing.

### Gate 7 — Audio post and captions

S09 owns transcript fidelity, timing provenance, subtitle segmentation, SRT/VTT validation, voice-first mix, music/SFX/ambience cues, rights and audio-processing instructions. SRT/VTT is emitted only if timecodes are supported. If an audio tool processes media, preserve original and processed artifact IDs and verify output; otherwise say specification only.

### Gate 8 — Composition and rendering

S10 edits and assembles scenes, assets, motion, overlays, subtitles and audio into a renderer-neutral composition contract; it specifies transitions, safe areas, audio mix and post-production steps before mapping the result to a target renderer. It may implement/execute a specific adapter only when explicitly requested, supported by the exact session, authorized and technically validated. Select `native`, `programmatic`, or `handoff` route after checking runtime, dependencies, fonts, codecs, file access, permissions and export. Proof render before full render when feasible. Do not install dependencies, access remote assets or send private content externally without authorization.

### Gate 9 — Independent dual QA

S12 first audits health/message/reference/continuity integrity. If actual audio/video/render files exist and inspection tools are available, it audits observable media properties: openability, metadata, dimensions, fps, duration, stream presence, sync, subtitle timing, blank frames, visual defects, voice intelligibility and rights. Mark each test `PASS`, `FAIL`, `PARTIAL`, `NOT_VERIFIED`, `NOT_RUN` or `NOT_APPLICABLE`. QA never passes unrun checks.

### Gate 10 — Delivery and correction

M00 aggregates stage results and emits exactly one delivery state. Targeted correction invalidates only affected dependents but must rerun all critical regression checks. Publish-ready is blocked by unresolved critical health claims, rights/consent, missing critical assets, invalid timing, broken media or unverified critical technical checks.

## 6. Change impact

- Source fact or health lock change → affected screenplay lines, overlays, scenes, reference prompts, captions, QA; route through S02.
- Transcript correction → affected segments, narrative mapping, scenes, subtitles, motion sync, render and QA; route through S09/S04/S06.
- Campaign/CTA change → screenplay, distribution copy, overlays, scenes, QA.
- MCG/Guide change → all affected reference prompts/assets/scenes/render and continuity QA; route through S13/S05.
- Scene segmentation change → motion, references, subtitles, sound cues, composition, render and QA.
- Design token change → affected visual assets/scenes/render and visual QA.
- Motion timing change → render and sync QA.
- Audio mix change → audio artifact and audio QA.
- Renderer setting/code change → render output and all technical verification.

Record `CHG-ID`, previous/new versions, reason, decision authority, impacted IDs, invalidated stages, tests to rerun and rollback/fallback. S14 maintains the conversation/source → context/requirement → owning artifact → change → dependent IDs → test/evidence → release disposition trace. Never silently rewrite accepted history or promote inferred preferences to requirements.

## 7. Output contract

Return a progressive package: executive project summary; source/health state; campaign/story; visual/continuity; scene/motion; audio/transcript/timing; subtitle/audio post; reference asset manifest; renderer and capability report; render evidence if any; distribution package; dual QA; blockers; final delivery state; human approvals still required.

Do not bury the user in every registry for a simple request. Provide full technical manifest and handoffs in `STANDARD`/`ADVANCED` mode.

## 8. Stop conditions

- No transcript invented when audio is unavailable.
- No exact timecode invented from reading speed.
- No unsupported medical claim, dosage, clinical recommendation or guaranteed outcome.
- No unsupported voice imitation or transfer of private audio without consent.
- No unlicensed music/SFX presented as cleared.
- No missing capabilities represented as available.
- No render/export claim without actual output evidence.
- No media QA PASS without observable inspection evidence.
- No human clinical/institutional approval or publication authorization claimed without authorized evidence.
- No `RENDERED_VERIFIED` when any critical verification is `NOT_VERIFIED`, `NOT_RUN`, `BLOCKED` or `FAIL`.

## 9. Release states

- `BLUEPRINT_ONLY`
- `REFERENCE_READY`
- `RENDER_READY`
- `RENDERED_PARTIALLY_VERIFIED`
- `RENDERED_VERIFIED`
- `BLOCKED`

Keep separate `human_approval_status`: `NOT_REQUESTED`, `PENDING`, `APPROVED`, `REJECTED`, `NOT_APPLICABLE`. Technical verification never substitutes for human approval.

## 10. Static quality gate

Before handoff, validate source-to-claim-to-message-to-scene-to-asset-to-overlay/audio-to-render traceability, timestamp provenance, MCG compatibility, asset rights/status, timeline arithmetic, manifest consistency, renderer assumptions, test evidence and delivery truth. Use `PASS`, `PASS_WITH_CAVEATS`, `HOLD`, or `FAIL`; dynamic host/renderer behavior requires real execution.


## S14 — mandatory conversation and release preflight

S14 classifies material context as EXPLICIT, CONFIRMED_PREFERENCE, INFERRED, PROPOSED, UNKNOWN or SUPERSEDED; records accessible source/date/scope and discloses inaccessible raw conversations/files. It never promotes an inference or proposal into a hard requirement.

For accepted changes, trace conversation/source → CTX/REQ → owner/artifact → change ID → dependency closure → tests/evidence → release disposition. Record old/new versions, changed skills/files, migration impact, positive/negative/edge/security/regression tests, rollback and approval revalidation.

Before GitHub publication, distinguish private Plugin Creator save/read-back, source branch, commit, PR, CI, independent review, merge, post-merge main CI and release. PR-head CI is not main CI. Public repository visibility is not a license. Never publish private assets, credentials or patient data. Keep repository and Plugin Creator visibility separate.

M00 retains orchestration and gate arbitration. S14 does not decide clinical truth, creative ownership, human authority or independent QA. See the [S14 skill](../conversation-release-audit/SKILL.md) and [M00/S14 integration contract](references/s14-integration-contract.md).

## Mandatory MCG integration gate — V4.1.6
Before S08 compiles still/reference prompts, verify one canonical MCG manifest, exactly seven Guide refs and three protocols, one primary owner per Guide, acyclic/resolvable dependencies, S02-only Health Truth references, adaptive continuity classes, exact model capability evidence, rights/privacy and artifact-bound human approvals. Mandatory order: S06 storyboard → S07 motion + S09 audio/time refs + S10 edit context → S13 refresh GUIDE-07/MCG → schema and semantic validation → S08. Affected scenes remain BLOCKED while refresh is NOT_RUN, BLOCKED, STALE or INVALIDATED.


## V4.1.7 motion, adapter and risk-proportional routing

Keep the existing ownership chain; do not add S15. S06 owns camera/shot design, S07 owns quantified element motion, S08 owns still/reference and optional video prompt adapters, S10 owns renderer translation, S12 owns independent QA, S13 owns continuity and M00 owns orchestration/gate arbitration. A beat sheet connects approved narrative/claim refs to scenes, shots, motion, audio, overlays and QA.

Use schemas/v4/motion-record.schema.json and scripts/validate_motion_contract.py. Validate half-open frame intervals, fps/timebase, units, timing source/precision, keyframes, phases, easing, path and S06 camera references. Platform-specific prompts require exact model/version evidence through the adapter schema; unknown capabilities stay UNKNOWN/NOT_CHECKED.

Risk-proportional R0–R3 routing may reduce duplicated process for genuinely low-risk, non-claim work after a pilot. It never skips intake/source scanning, S02 review of health claims, rights/privacy/consent, applicable MCG continuity, independent S12 QA or required human approval. Unknown risk is not low risk. Any gate escape, misclassification or critical defect stops the pilot and restores the stricter route.



## V4.1.8 risk-lane routing and controlled pilot

Before Gate 0, M00 records a project risk assessment across health harm, audience vulnerability, evidence uncertainty, privacy/consent, rights/authority, reach/reversibility and production integrity. Highest credible lane wins; a critical trigger forces R3; UNKNOWN material risk is at least R2 and never R0. R0 requires S02's explicit no-material-health-claim disposition. R1 remains on the standard evidence and QA route. R2 requires full evidence and specialist/human review. R3 stops affected work and escalates to an authorized human. No lane waives S02, S12, rights/privacy/consent, continuity or applicable human approval. See docs/risk-routing-r0-r3-v4.1.8.md.

R0/R1 fast-track is inactive until written sponsor approval, named owner, S02/S12 concurrence, privacy-minimized logging, baseline, shadow adjudication and rollback readiness. R2/R3 are excluded. See docs/pilot-kpi-baseline-v4.1.8.md.

## V4.1.8 beat-sheet integration

M00 requires a beat-sheet trace from approved source/message/claim refs through beat, scene/shot, S07 motion/element, S09 audio, overlays/transitions, S10 renderer layers and S12 QA oracles. S04 owns narrative function; S06 shot/camera; S07 motion; S09 audio timing; S10 mapping; S13 continuity; S12 independent QA. Validate with schemas/v4/beat-sheet.schema.json and scripts/validate_beat_sheet.py. Exact timing must retain source provenance; estimated timing cannot be upgraded downstream.

## V4.1.8 renderer target boundary

Remotion is the first concrete renderer mapping target, owned by S10. The mapping design is not execution evidence. Package/version pinning, typecheck, bundle, render, MP4 inspection and independent S12 media QA remain NOT_RUN until performed against an exact runtime and artifact.
## V4.1.9 — governed learning, drift and risk-proportional preflight

Before any repository/skill evaluation or versioned release change, S14 remains a mandatory cross-cutting preflight. It must disclose source coverage, identity/parity uncertainty, superseded decisions and missing evidence. The contract is docs/learning-asset-drift-and-outcome-contract-v4.1.9.md.

M00 orchestrates four existing functions; it does not add a new specialist or production gate:
1. AFL: S01 captures source/rights/provenance; S08 compiles and reuses only APPROVED records; S12 independently checks the reusable recipe; S13 contributes only continuity dependencies; S02 alone reviews current health claims.
2. MDS: S14 records observed external changes and accepted-baseline decisions; S08 assesses per-feature impact. Drift detection never changes a model to supported or runtime-tested automatically.
3. MSA: S08 may return up to three evidence-bound candidates as advice only. The user/project owner remains the selector; unknown features stay UNKNOWN/NOT_CHECKED.
4. POR: M00 aggregates privacy-minimized process metrics with numerator, denominator, cohort, period, evidence and limitations. Do not collect new audience/patient behavioral-health data or infer health outcomes.

Risk-proportional preflight changes only the depth of additional review and duplicate clerical capture. S14's baseline preflight remains mandatory for every lane. Preserve highest-lane-wins, R3 critical override, UNKNOWN material risk >= R2, no averaging away a critical trigger, explicit S02 no-material-claim disposition for R0, and full R2/R3 isolation. R0/R1 fast-track stays inactive until written sponsor authorization, owner, S02/S12 concurrence, privacy/rights review, measured baseline, shadow adjudication and rollback readiness.

Never promote CANDIDATE, UNKNOWN, STALE, NOT_RUN, NOT_VERIFIED, HOLD or BLOCKED to APPROVED/PASS from a summary, prompt quality, hash change, unit test or version label. Changes to source, claim, model/version, rights, MCG lock, motion, renderer or QA oracle invalidate dependent records and require new evidence.
