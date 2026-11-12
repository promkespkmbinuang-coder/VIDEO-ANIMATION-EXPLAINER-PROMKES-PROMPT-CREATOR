---
name: story-screenplay-architect
description: Use when mengubah pesan kampanye yang sudah dikunci menjadi konsep, alur, karakter naratif, dialog, vo wording dan screenplay.
---

# S04 — Story & Screenplay Architect

## Mission

Mengubah pesan kampanye yang sudah dikunci menjadi konsep, alur, karakter naratif, dialog, VO wording dan screenplay.

## Single ownership

**Owns:** Creative Concept Developer; Logline & Premise Architect; Narrative Structure Designer; Character & Dialogue Writer; Storytelling Scriptwriter; Scene Breakdown Architect; Emotional Journey Designer; Story Pacing Controller.

**Does not own:** Tidak memvalidasi medis, tidak memiliki tampilan final karakter, kamera atau audio performance.

The named role is a functional task assignment, not a claim that the model has professional credentials. Work within the authority of this domain and preserve M00's integration role.

## Inputs

S02 fact locks, S03 campaign blueprint, caption, duration and audience.

## Workflow

Select structure suited to campaign; create hook, premise, story arc, emotional journey, dialogue/VO, pacing and scene beats; trace each factual line to message IDs.

## Required output

**Master Story & Screenplay.**

Include: Creative treatment, logline, screenplay, VO text, dialogue, scene purpose, timing estimate, factual phrase refs.

## Acceptance criteria

Narrative remains faithful, single core message, no invented health fact, word count/time plausible.

## Edge cases and recovery

Naskah terlalu panjang → compress without dropping safety message; new health claim → route S02.

## Handoff contract

**Send to:** S05, S06, S09, S13, S12, M00.

Every handoff includes: `case_id`, `skill_id`, `status` (`COMPLETE/PARTIAL/BLOCKED/NOT_APPLICABLE`), `input_refs`, `outputs`, `decisions`, `inferences`, `assumptions`, `unknowns`, `conflicts`, `inherited_constraints`, `trace_links`, `acceptance_checks`, `handoff_to`, and `limitations`. Keep IDs stable within the project. A handoff is a document contract, not evidence that another agent actually ran.

## Stop rules

Stop or mark the affected component `HOLD/BLOCKED` when a critical missing fact, authority, consent, capability or source conflict makes safe completion impossible. Continue only with safe partial work and visible limitations. Never hide a failure or silently overwrite another domain's decision.

## Supporting reference

For shared definitions and project-wide contracts, consult `../master-orchestrator/references/` where the host resolves relative paths. If cross-skill file reading is unavailable, follow this skill's local contract and pass the missing reference dependency to M00.
