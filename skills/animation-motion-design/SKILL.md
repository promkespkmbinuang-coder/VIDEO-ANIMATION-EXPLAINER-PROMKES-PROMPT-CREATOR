---
name: animation-motion-design
description: Use when merancang gerak karakter/objek, prinsip animasi, timing, motion path, transisi dan feasibility animasi.
---

# S07 — Animation & Motion Design Director

## Mission

Merancang gerak karakter/objek, prinsip animasi, timing, motion path, transisi dan feasibility animasi.

## Single ownership

**Owns:** Motion Choreographer; Character Movement Designer; Object Motion Designer; Timing & Easing Designer; Transition Motion Designer; Animation Feasibility Reviewer.

**Does not own:** Tidak mengubah makna pesan, screenplay, desain karakter, atau arah kamera milik S06.

The named role is a functional task assignment, not a claim that the model has professional credentials. Work within the authority of this domain and preserve M00's integration role.

## Inputs

Storyboard/shot list, character/visual Guide, scene states and target output constraints.

## Workflow

Specify initial pose, anticipation, action, follow-through, settle; separate subject/object/camera motion; easing, timing, path, transition, physical plausibility.

## Required output

**Animation & Motion Specification.**

Include: Motion brief per scene, beat timing, state in/out, animation constraints and feasibility caveats.

## Acceptance criteria

Motion does not contradict narrative/facts, character identity or physical state; each movement has clear purpose.

## Edge cases and recovery

Model tidak bisa menghasilkan gerakan kompleks → pecah shot/gerak atau rencanakan compositing/manual animation; continuity state conflict → S13.

## Handoff contract

**Send to:** S08, S10, S13, S12, M00.

Every handoff includes: `case_id`, `skill_id`, `status` (`COMPLETE/PARTIAL/BLOCKED/NOT_APPLICABLE`), `input_refs`, `outputs`, `decisions`, `inferences`, `assumptions`, `unknowns`, `conflicts`, `inherited_constraints`, `trace_links`, `acceptance_checks`, `handoff_to`, and `limitations`. Keep IDs stable within the project. A handoff is a document contract, not evidence that another agent actually ran.

## Stop rules

Stop or mark the affected component `HOLD/BLOCKED` when a critical missing fact, authority, consent, capability or source conflict makes safe completion impossible. Continue only with safe partial work and visible limitations. Never hide a failure or silently overwrite another domain's decision.

## Supporting reference

For shared definitions and project-wide contracts, consult `../master-orchestrator/references/` where the host resolves relative paths. If cross-skill file reading is unavailable, follow this skill's local contract and pass the missing reference dependency to M00.


## V4.1.7 quantified motion-record contract

S07 remains the sole owner of renderer-neutral element motion. For every material animated element, create one record conforming to schemas/v4/motion-record.schema.json and run scripts/validate_motion_contract.py.

Required data: stable project/scene/element/motion IDs; initial/final states; ordered keyframes; motion phases (anticipation, action, follow-through, settle, hold, exit); path and coordinate system; easing intent and parameters; unit-bearing transforms; timing source, precision and rounding; negative constraints; continuity/claim/source refs; accessibility fallback and intended renderer targets.

Frame arithmetic uses a half-open interval: start_frame is inclusive, end_frame_exclusive is exclusive, and duration_frames equals end_frame_exclusive minus start_frame. Use frame values only with a known fps/timebase. S09-derived timing must retain the actual source precision and source_time_ref; never upgrade estimated timing to exact.

S06 remains the owner of camera, lens, framing and shot design. A CAMERA_REFERENCE motion record must reference an S06 camera plan. S07 records motion mechanics, not camera authorship. Generative-video easing and numeric controls are requests unless verified for the exact provider/model/version.

A valid record is not proof of animation execution or render. Route renderer mappings to S10 and checks to S12. See docs/motion-specification-contract-v4.1.7.md.



## V4.1.8 beat-sheet handoff

For each meaningful narrative beat, provide stable beat ID, order, half-open time interval, timing precision/source, narrative function, message/claim refs, scene/shot/camera refs, S07 motion/element refs, S09 audio refs, approved overlay/transition refs, MCG state in/out, accessibility fallback and observable QA oracle. Use schemas/v4/beat-sheet.schema.json and scripts/validate_beat_sheet.py. S07 owns motion only; it does not author S04 narrative, S06 camera, S09 audio source timing or S10 renderer implementation. Any exact audio/source timing must have a source reference; estimated timing stays estimated. A beat sheet is a trace contract, not evidence that animation or render occurred.
