---
name: quality-assurance-controller
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


## V4.1.7 cinematic and motion QA extension

Integrate cinematic/motion checks into existing S12 QA levels. Do not add a duplicate release gate or new owner. For static package QA, inspect the S07 schema and semantic contract: half-open frame arithmetic, keyframe order/range, phase bounds, units, easing parameters, timing provenance/precision, negative constraints, S06 camera-plan refs, continuity refs and accessibility fallback.

Cinematic criteria must be observable and assigned an oracle. Minimum checks:
- narrative and beat function mapped to approved message/claim refs;
- shot/framing/camera intent matches the S06 shot contract;
- subject/object/environment motion readability and state arc;
- exact duration arithmetic and timing precision consistent with S09 evidence;
- transition purpose and scene-in/out continuity against MCG/S13;
- no visual mutation of locked claims, names, dates, logo or CTA overlays;
- no unintended flicker, deformation, clipping, unsafe crop or unreadable text;
- accessibility, reduced-motion behavior and sufficient reading time;
- target model/renderer controls are supported by exact versioned evidence.

Each criterion records expected and observed result, status, evidence refs, limitation, defect ID, owner, correction and retest. Avoid subjective aesthetic scoring as an acceptance oracle. Static contract PASS does not imply model runtime, renderer integration, render, MP4 inspection or human approval. Missing media remains NOT_RUN; inaccessible properties remain NOT_VERIFIED.
