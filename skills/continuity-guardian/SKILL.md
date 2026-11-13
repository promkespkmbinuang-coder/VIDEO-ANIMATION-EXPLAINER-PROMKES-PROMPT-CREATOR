---
name: continuity-guardian
description: Use when membangun dan mengelola mcg sebagai indeks kontrol proyek untuk menjaga identitas kreatif, scene state, versioning dan hubungan lintas-domain.
---

# S13 — Character, Narrative & Style Continuity Guardian

## Mission

Membangun dan mengelola MCG sebagai indeks kontrol proyek untuk menjaga identitas kreatif, scene state, versioning dan hubungan lintas-domain.

## Single ownership

**Sole ownership:** project MCG canonical manifest/index; registry of exactly seven Guide refs; three protocol refs; stable lock references; dependency/change index; and GUIDE-07 integrated Scene Continuity ledger. S13 does not author GUIDE-01 through GUIDE-06, health claims, screenplay, visual canon, audio source records, motion or renderer code.

**Does not own:** Tidak mengambil alih domain authoring S04/S05/S06/S07/S09/S10; tidak mengklaim actual asset created if only specification exists.

The named role is a functional task assignment, not a claim that the model has professional credentials. Work within the authority of this domain and preserve M00's integration role.

## Canonical single-owner map

| Guide | Sole primary owner |
|---|---|
| GUIDE-01 Master Character (visual identity) | S05 visual-identity-art-direction |
| GUIDE-02 Character Personality & Narrative Profile | S04 story-screenplay-architect |
| GUIDE-03 Master Visual Style | S05 visual-identity-art-direction |
| GUIDE-04 Master Narrative Style | S04 story-screenplay-architect |
| GUIDE-05 Master Voice & Audio | S09 voice-sound-design |
| GUIDE-06 Master World & Environment | S05 visual-identity-art-direction |
| GUIDE-07 Scene Continuity | S13 continuity-guardian |

S06/S07/S09/S10 contribute bounded scene, motion, audio and edit data; they are not co-owners. S02 solely owns Health Truth Registry and Fact Lock.

## Three mandatory protocols

GCL-01 Global Continuity Lock; CCM-01 Continuity Change Management; CQA-01 Continuity Quality Assurance.

## Mandatory post-storyboard gate

S06 storyboard → S07 motion + S09 audio/time references + S10 edit context → S13 refresh GUIDE-07 and MCG → validate locks, dependency graph and scene contract → S08 still/reference compilation. Block affected S08 scenes while refresh is NOT_RUN, BLOCKED, STALE or INVALIDATED. Still prompts describe one captured visual state; temporal motion stays in S07.

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


## Health Truth Preservation
S13 stores claim IDs, statuses, source/evidence refs and hashes only. It must not copy or rewrite claim text. S02 alone interprets evidence and approves safe/forbidden wording.

## Adaptive continuity
Classify attributes as IMMUTABLE, CONTROLLED_VARIATION or SCENE_DEPENDENT. Missing state is not permission to invent a variation. Track character identity, narrative, visual, voice/audio, world/environment and scene state through owner references.

## Acceptance
No duplicate canonical source; exactly seven Guides and three protocols; one owner per Guide; no broken refs or dependency cycles; LOCKED bound to authorized human approval and exact hash; no health-fact mutation; exact target capability evidence; S13 refresh before S08; no PASS without execution evidence.
