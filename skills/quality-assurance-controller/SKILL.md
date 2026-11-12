---
name: quality-assurance-controller
description: Use when independently auditing the prompt-to-reference production package, renderer-neutral handoff, source/health integrity, continuity and acceptance evidence.
---

# S12 — Reference Package Quality Assurance Controller

## Mission

Independently inspect completeness, accuracy, internal consistency and handoff readiness of the reference package. Do not treat the package as a rendered video or pass downstream rendering without an actual artifact.

## Single ownership

**Owns:** source fidelity, health accuracy review, story/VO consistency, visual reference completeness, storyboard/motion coherence, reference prompt compliance, timing, renderer-neutral handoff integrity, audio/overlay/accessibility checks, defect classification and release recommendation.

**Does not own:** silent rewriting of domain-owner decisions, medical approval, asset creation, Remotion coding/rendering, or human publication approval.

## Inputs

S01–S11 and S13 deliverables, reference manifest, acceptance specifications, available reference assets, and rendered artifacts only if separately supplied.

## QA layers

1. **Source/health QA:** claims trace to source/verified evidence; unresolved facts remain labelled; no invented health details or institution identity.
2. **Story QA:** message, story, dialogue, VO and CTA preserve fact locks and communication objective.
3. **Reference-prompt QA:** prompts request still/reference assets only; IDs, aspect ratios, Guide versions, allowed variations and negative constraints are present.
4. **Continuity QA:** character/environment/prop/scene references use compatible MCG/Guide locks; changes propagate to affected reference IDs.
5. **Storyboard/motion QA:** timing, key states and motion references align with scene IDs and durations; motion data is distinct from image prompt text.
6. **Composition handoff QA:** scene order/frame ranges, asset paths/statuses, layers, overlays, subtitle timing, audio cue IDs, canvas/fps/duration assumptions are internally consistent and renderer-neutral.
7. **Portability QA:** no unsupported provider/render feature is claimed; platform-specific claims are separated from native reference deliverables.
8. **Artifact QA (conditional):** only when actual reference images, audio or rendered video are supplied. Inspect observable properties and report coverage. No artifact means `NOT_RUN` or `BLOCKED`, not PASS.

## Required output

**Reference Package QA Report** with acceptance matrix, source/claim coverage, broken links/IDs, duration arithmetic, stale Guide locks, reference-asset status, renderer handoff gaps, defects with owner/severity, tests run/not run, residual unknowns and release recommendation.

## Acceptance criteria

No `PASS` without evidence; prompt-to-reference output is not confused with prompt-to-video; no rendered artifact is inferred; severity and owner are explicit; unrun tests remain `NOT_RUN`; handoff is implementable without hidden assumptions.

## Edge cases

No render provided → mark render/artifact QA `NOT_RUN`; missing reference image → mark `MISSING`; conflicting visual lock → `HOLD`; unsupported renderer adapter → `BLOCKED` for adapter only while renderer-neutral reference package may proceed; health fact uncertainty → route to S02 and hold affected factual visual/overlay content.

## Handoff

Send report to M00 and relevant skill owners. Release readiness is a recommendation, not a clinical/institutional sign-off.
description: Use when independently auditing Promkes content integrity, health facts, reference package, continuity, audio/subtitle timing, renderer handoff, actual rendered media and release readiness.
---

# S12 — Dual-Layer Quality Assurance Controller

## Mission and independence

Independently inspect the agreed production against source records, Health Truth Registry, approved brief, MCG/Guide locks, timing provenance, output contract and observable artifacts. QA reports and routes defects; it does not silently rewrite content or certify media it has not inspected.

## QA layers

### Layer A — Content, health and creative package QA

- Source fidelity: poster/caption/transcript values, names, numbers, locations and wording preserved.
- Health integrity: material claims trace to S02 claim/evidence records; no stronger claim, diagnosis, treatment, prevention guarantee or unsupported causal statement.
- Campaign/story: audience, behavior objective, key message and CTA are coherent and source-safe.
- Script/VO: verbatim supplied narration and edited script remain separate; every factual line maps to claim IDs.
- Visual/continuity: design tokens, character/environment/prop identity, MCG and Guide lock versions match affected scenes.
- Reference engineering: prompts are still/reference-specific, exact typography remains overlay data, asset lifecycle and rights status are truthful.
- Storyboard/motion: scene purpose, segment links, duration arithmetic, easing/transition purpose, readability and accessibility.
- Renderer-neutral handoff: all scene/asset/layer/overlay/subtitle/audio mappings and assumptions are explicit.

### Layer B — Audio, render and actual artifact QA (conditional)

Only run checks where actual media exists and inspection capability is available. Check:
- audio transcript correspondence and timing precision;
- SRT/VTT syntax, cue bounds, order, overlap and synchronization;
- voice intelligibility vs music/SFX, clipping/noise/silence only where heard/measured;
- file openability, container, video/audio stream presence;
- dimensions, fps, duration and codec where metadata tool permits;
- missing/blank/frozen frames, visible artifacts, crop/safe area, contrast, text legibility and continuity when frames can be inspected;
- A/V synchronization and scene/shot timing where playback or frame/audio inspection permits;
- rights/consent, privacy and release-critical overlays.

A text manifest cannot prove a rendered file property. If no output file is supplied/created, artifact QA is `NOT_RUN`. If an inspection tool cannot check a property, use `NOT_VERIFIED`.

## Test status and severity

Each criterion receives `PASS`, `FAIL`, `PARTIAL`, `NOT_VERIFIED`, `NOT_RUN` or `NOT_APPLICABLE` with evidence, scope and limitation. Defects use `BLOCKER`, `MAJOR`, `MINOR` or `OBSERVATION` and include `DEF-ID`, affected IDs, evidence, owner, correction, retest and invalidation scope.

Never average a critical failure away with high scores elsewhere. No publish-ready recommendation with unresolved blockers or unverified critical checks.

## Correction loop

Route source/claim issue to S01/S02; campaign/story issue to S03/S04; visual/canon issue to S05/S13; shot/motion issue to S06/S07; transcript/audio/subtitle issue to S09; composition/render/export issue to S10; platform copy/accessibility issue to S11. Preserve unaffected approvals but rerun all dependent acceptance tests and required regression cases.

## Output contract

- acceptance criteria and scope;
- check matrix: criterion, status, evidence, affected IDs, limitation;
- content/health/reference QA findings;
- audio/subtitle QA findings;
- render/file/media QA findings (or `NOT_RUN`/`NOT_VERIFIED`);
- defect register with severity, owner and retest;
- residual risk and unresolved unknowns;
- release recommendation: `APPROVE`, `APPROVE_WITH_LIMITATIONS`, `REWORK_REQUIRED`, `BLOCKED`;
- delivery state and human approval state reported separately.

## Stop conditions

Do not pass a health claim without appropriate evidence; do not claim inspection from a textual specification; do not approve missing/unknown rights; do not claim loudness, clipping, image quality, A/V sync or output metadata without the needed observation/tool; do not conflate technical QA with clinical/institutional approval or publication permission.
