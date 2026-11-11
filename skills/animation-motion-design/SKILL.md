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
