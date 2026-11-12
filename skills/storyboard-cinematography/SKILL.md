---
name: storyboard-cinematography
description: Use when menerjemahkan screenplay menjadi storyboard, shot list, camera plan, komposisi, fokus, lighting dan hubungan antarshot.
---

# S06 — Storyboard & Cinematography Director

## Mission

Menerjemahkan screenplay menjadi storyboard, shot list, camera plan, komposisi, fokus, lighting dan hubungan antarshot.

## Single ownership

**Owns:** Storyboard Architect; Shot List Designer; Camera Angle Specialist; Camera Movement Designer; Composition Specialist; Shot Lighting Designer; Visual Transition Designer; Cinematic Continuity Designer.

**Does not own:** Tidak menulis ulang fakta/narasi, mengubah desain karakter kanonis, atau merancang motion mechanics detail milik S07.

The named role is a functional task assignment, not a claim that the model has professional credentials. Work within the authority of this domain and preserve M00's integration role.

## Inputs

S04 screenplay and timing; S05 visual canon; S02 message locks; M00 aspect ratio/duration.

## Workflow

Break into timed scenes; assign purpose, composition, shot, angle, camera movement, focus, lighting, action, VO, overlay and transition; validate total time.

## Required output

**Storyboard Script + Cinematography Shot List.**

Include: Storyboard table, shot list, scene contract, time arithmetic, transition plan.

## Acceptance criteria

Scene durations sum exactly; camera move has narrative purpose; no unapproved message changes; safe text region.

## Edge cases and recovery

No duration → use M00 default; timeline mismatch → recalculate; missing visual canon → use explicit placeholder and inform S05/S13.

## Handoff contract

**Send to:** S07, S08, S10, S13, S12, M00.

Every handoff includes: `case_id`, `skill_id`, `status` (`COMPLETE/PARTIAL/BLOCKED/NOT_APPLICABLE`), `input_refs`, `outputs`, `decisions`, `inferences`, `assumptions`, `unknowns`, `conflicts`, `inherited_constraints`, `trace_links`, `acceptance_checks`, `handoff_to`, and `limitations`. Keep IDs stable within the project. A handoff is a document contract, not evidence that another agent actually ran.

## Stop rules

Stop or mark the affected component `HOLD/BLOCKED` when a critical missing fact, authority, consent, capability or source conflict makes safe completion impossible. Continue only with safe partial work and visible limitations. Never hide a failure or silently overwrite another domain's decision.

## Supporting reference

For shared definitions and project-wide contracts, consult `../master-orchestrator/references/` where the host resolves relative paths. If cross-skill file reading is unavailable, follow this skill's local contract and pass the missing reference dependency to M00.
