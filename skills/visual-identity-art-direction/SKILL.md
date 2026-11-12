---
name: visual-identity-art-direction
description: Use when membangun identitas visual kanonis untuk karakter, gaya seni, palet, lokasi, lingkungan dan props.
---

# S05 — Visual Identity & Art Direction

## Mission

Membangun identitas visual kanonis untuk karakter, gaya seni, palet, lokasi, lingkungan dan props.

## Single ownership

**Owns:** Art Style Director; Color & Shape Language Designer; Character Designer; Character Consistency Architect; Environment Designer; Props & Object Designer; Visual Metaphor Designer; Brand Integration Designer.

**Does not own:** Tidak mengubah substansi cerita, mengatur angle kamera, atau menyetujui klaim kesehatan.

The named role is a functional task assignment, not a claim that the model has professional credentials. Work within the authority of this domain and preserve M00's integration role.

## Inputs

S01 visual/brand dossier, S04 story character needs, campaign style constraints and rights information.

## Workflow

Define style grammar, palette, forms, character features/proportions/wardrobe, environment, prop registry, lighting/rendering and allowed variations.

## Required output

**Master Visual Style Guide + Character/Environment/Prop references.**

Include: Visual Guide, character profiles/sheets, location/prop IDs, palette and reference asset plan.

## Acceptance criteria

Distinct stable IDs; consistent descriptions and versions; real person depiction only with basis/permission; no unauthorised logo recreation.

## Edge cases and recovery

Brand/likeness unclear → generic representation; reference asset missing → PROPOSED/DRAFT; inconsistent direction → HOLD for owner decision.

## Handoff contract

**Send to:** S13, S06, S07, S08, S12, M00.

Every handoff includes: `case_id`, `skill_id`, `status` (`COMPLETE/PARTIAL/BLOCKED/NOT_APPLICABLE`), `input_refs`, `outputs`, `decisions`, `inferences`, `assumptions`, `unknowns`, `conflicts`, `inherited_constraints`, `trace_links`, `acceptance_checks`, `handoff_to`, and `limitations`. Keep IDs stable within the project. A handoff is a document contract, not evidence that another agent actually ran.

## Stop rules

Stop or mark the affected component `HOLD/BLOCKED` when a critical missing fact, authority, consent, capability or source conflict makes safe completion impossible. Continue only with safe partial work and visible limitations. Never hide a failure or silently overwrite another domain's decision.

## Supporting reference

For shared definitions and project-wide contracts, consult `../master-orchestrator/references/` where the host resolves relative paths. If cross-skill file reading is unavailable, follow this skill's local contract and pass the missing reference dependency to M00.
