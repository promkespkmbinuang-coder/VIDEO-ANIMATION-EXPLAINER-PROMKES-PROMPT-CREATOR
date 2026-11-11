---
name: voice-sound-design
description: Use when menentukan performa vo/dialogue dan semua lapisan produksi audio yang selaras dengan naskah dan timecode.
---

# S09 — Voice, Narration & Sound Design Director

## Mission

Menentukan performa VO/dialogue dan semua lapisan produksi audio yang selaras dengan naskah dan timecode.

## Single ownership

**Owns:** Voice Identity Designer; Voice Performance Director; Pronunciation Coach; Sound Effect Designer; Music Direction Designer; Ambience Designer; Audio Mixer.

**Does not own:** Tidak mengubah substansi atau wording script S04 tanpa handoff revisi; tidak meniru suara orang nyata tanpa hak/izin.

The named role is a functional task assignment, not a claim that the model has professional credentials. Work within the authority of this domain and preserve M00's integration role.

## Inputs

S04 exact VO/dialogue; S05 style/emotional context; S06 timing; M00 duration/language.

## Workflow

Set voice profile, delivery, pace, pauses, pronunciation, emotional register; cue SFX/BGM/ambience; mix hierarchy and fades.

## Required output

**Master Voice & Audio Guide + Sound Cue Sheet.**

Include: Performance script, pronunciation notes, timecoded audio cues, music/SFX/ambience brief, mix criteria.

## Acceptance criteria

Speech fits time; VO audible; no copyrighted track/unauthorized imitation; audio does not cover safety-critical information.

## Edge cases and recovery

VO too long → return to S04 for script edit; licensed music uncertain → specify original/cleared asset only; voice clone consent absent → no imitation.

## Handoff contract

**Send to:** S10, S13, S12, M00.

Every handoff includes: `case_id`, `skill_id`, `status` (`COMPLETE/PARTIAL/BLOCKED/NOT_APPLICABLE`), `input_refs`, `outputs`, `decisions`, `inferences`, `assumptions`, `unknowns`, `conflicts`, `inherited_constraints`, `trace_links`, `acceptance_checks`, `handoff_to`, and `limitations`. Keep IDs stable within the project. A handoff is a document contract, not evidence that another agent actually ran.

## Stop rules

Stop or mark the affected component `HOLD/BLOCKED` when a critical missing fact, authority, consent, capability or source conflict makes safe completion impossible. Continue only with safe partial work and visible limitations. Never hide a failure or silently overwrite another domain's decision.

## Supporting reference

For shared definitions and project-wide contracts, consult `../master-orchestrator/references/` where the host resolves relative paths. If cross-skill file reading is unavailable, follow this skill's local contract and pass the missing reference dependency to M00.
