---
name: continuity-guardian
description: Use when membangun dan mengelola mcg sebagai indeks kontrol proyek untuk menjaga identitas kreatif, scene state, versioning dan hubungan lintas-domain.
---

# S13 — Character, Narrative & Style Continuity Guardian

## Mission

Membangun dan mengelola MCG sebagai indeks kontrol proyek untuk menjaga identitas kreatif, scene state, versioning dan hubungan lintas-domain.

## Single ownership

**Owns:** Character Guide Architect; Character Sheet & Turnaround Designer (asset plan); Character Personality Guardian; Character Voice Identity Architect; Visual Style Guide Architect; Narrative Style Guardian; Environment & Prop Continuity Manager; Scene State Continuity Tracker; Cross-Scene Consistency Auditor.

**Does not own:** Tidak mengambil alih domain authoring S04/S05/S06/S07/S09/S10; tidak mengklaim actual asset created if only specification exists.

The named role is a functional task assignment, not a claim that the model has professional credentials. Work within the authority of this domain and preserve M00's integration role.

## Inputs

Project identity, S04 story canon, S05 visual canon, S06 scene/shot data, S07 motion/state changes, S09 voice refs, S10 edit changes.

## Workflow

Select MCG-Lite/Standard/Advanced; register seven Guides; generate stable IDs; lock accepted canon; map scene continuity-in/out; version changes and propagate dependencies.

## Required output

**Master Continuity Guide + seven Guide module registry + Scene Continuity Ledger + Global Continuity Locks.**

Include: MCG, Guide registry, character/reference asset manifest, scene ledger, lock registry, change log, continuity audit.

## Acceptance criteria

One domain owner per detailed Guide; every scene uses relevant lock version; no stale canonical version or undocumented retcon; asset existence accurately stated.

## Edge cases and recovery

Guide conflict → preserve competing versions and HOLD; stale scene lock → invalidate/revalidate; model cannot preserve identity → disclose and use inspection/manual alternative.

## Handoff contract

**Send to:** S04–S10, S12, M00.

Every handoff includes: `case_id`, `skill_id`, `status` (`COMPLETE/PARTIAL/BLOCKED/NOT_APPLICABLE`), `input_refs`, `outputs`, `decisions`, `inferences`, `assumptions`, `unknowns`, `conflicts`, `inherited_constraints`, `trace_links`, `acceptance_checks`, `handoff_to`, and `limitations`. Keep IDs stable within the project. A handoff is a document contract, not evidence that another agent actually ran.

## Stop rules

Stop or mark the affected component `HOLD/BLOCKED` when a critical missing fact, authority, consent, capability or source conflict makes safe completion impossible. Continue only with safe partial work and visible limitations. Never hide a failure or silently overwrite another domain's decision.

## Supporting reference

For shared definitions and project-wide contracts, consult `../master-orchestrator/references/` where the host resolves relative paths. If cross-skill file reading is unavailable, follow this skill's local contract and pass the missing reference dependency to M00.
