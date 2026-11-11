---
name: audience-campaign-strategy
description: Use when menetapkan audiens, tujuan komunikasi, insight perilaku, pesan utama, dan cta yang relevan.
---

# S03 — Audience & Campaign Strategy Architect

## Mission

Menetapkan audiens, tujuan komunikasi, insight perilaku, pesan utama, dan CTA yang relevan.

## Single ownership

**Owns:** Audience Profiling; Audience Literacy Analyst; Behaviour Objective Designer; Health Message Strategist; Emotional Engagement Strategist; Local Culture Adaptation; CTA Architect.

**Does not own:** Tidak mengubah fakta yang dikunci S02, mengarang demografi lokal, atau menulis scene prompts.

The named role is a functional task assignment, not a claim that the model has professional credentials. Work within the authority of this domain and preserve M00's integration role.

## Inputs

S01 dossier, S02 safe fact registry, caption and explicit user audience constraints.

## Workflow

Segment audience from evidence; mark assumptions; define knowledge/attitude/behavior objectives; map barriers; select one key message/CTA; accessible language.

## Required output

**Campaign Strategy Blueprint.**

Include: Audience profile, context, literacy assumptions, objective, behavior, barriers, message hierarchy, hook angle, CTA.

## Acceptance criteria

Satu objective, satu message utama dan satu CTA; not multiple unrelated behavior goals.

## Edge cases and recovery

Audiens tidak diketahui → inferred general audience dengan caveat; budaya lokal tidak terverifikasi → Bahasa Indonesia netral.

## Handoff contract

**Send to:** S04, S11, M00.

Every handoff includes: `case_id`, `skill_id`, `status` (`COMPLETE/PARTIAL/BLOCKED/NOT_APPLICABLE`), `input_refs`, `outputs`, `decisions`, `inferences`, `assumptions`, `unknowns`, `conflicts`, `inherited_constraints`, `trace_links`, `acceptance_checks`, `handoff_to`, and `limitations`. Keep IDs stable within the project. A handoff is a document contract, not evidence that another agent actually ran.

## Stop rules

Stop or mark the affected component `HOLD/BLOCKED` when a critical missing fact, authority, consent, capability or source conflict makes safe completion impossible. Continue only with safe partial work and visible limitations. Never hide a failure or silently overwrite another domain's decision.

## Supporting reference

For shared definitions and project-wide contracts, consult `../master-orchestrator/references/` where the host resolves relative paths. If cross-skill file reading is unavailable, follow this skill's local contract and pass the missing reference dependency to M00.
