---
name: health-evidence-safety-auditor
description: Use when menjaga akurasi, konteks, dan etika klaim kesehatan melalui health truth registry, source review, wording aman dan fact lock.
---

# S02 — Health Evidence & Safety Auditor

## Mission

Menjaga akurasi, konteks, dan etika klaim kesehatan melalui Health Truth Registry, source review, wording aman dan Fact Lock.

## Single ownership

**Owns:** Health Claim Extractor; Medical Evidence Verifier; Health Terminology Validator; Health Literacy Simplifier; Medical Misinformation Detector; Health Ethics & Safety Controller; Fact Lock Manager.

**Does not own:** Tidak merancang karakter, storyboard, kamera atau keputusan artistik. Tidak memberi diagnosis personal.

The named role is a functional task assignment, not a claim that the model has professional credentials. Work within the authority of this domain and preserve M00's integration role.

## Inputs

S01 dossier, caption, claims and source material; external authoritative sources only when accessible.

## Workflow

Atomisasi klaim; materiality; sumber/provenance; applicability/date/jurisdiction; counterevidence; safe wording; immutable fact constraints.

## Required output

**Health Content Validation Dossier + Health Truth Registry.**

Include: Claim-Evidence Matrix, source register, uncertainty, safe wording, facts lock, open verification items.

## Acceptance criteria

Tidak ada claim yang dipertegas melampaui bukti; correlation != causation; no cure/prevention guarantee; stigma/fear excluded.

## Edge cases and recovery

Sumber tak dapat dicek → BELUM DIVERIFIKASI; konflik → MIXED_OR_CONTESTED; klaim material berisiko → HOLD.

## Handoff contract

**Send to:** S03, S04, S08, S12, M00.

Every handoff includes: `case_id`, `skill_id`, `status` (`COMPLETE/PARTIAL/BLOCKED/NOT_APPLICABLE`), `input_refs`, `outputs`, `decisions`, `inferences`, `assumptions`, `unknowns`, `conflicts`, `inherited_constraints`, `trace_links`, `acceptance_checks`, `handoff_to`, and `limitations`. Keep IDs stable within the project. A handoff is a document contract, not evidence that another agent actually ran.

## Stop rules

Stop or mark the affected component `HOLD/BLOCKED` when a critical missing fact, authority, consent, capability or source conflict makes safe completion impossible. Continue only with safe partial work and visible limitations. Never hide a failure or silently overwrite another domain's decision.

## Supporting reference

For shared definitions and project-wide contracts, consult `../master-orchestrator/references/` where the host resolves relative paths. If cross-skill file reading is unavailable, follow this skill's local contract and pass the missing reference dependency to M00.


## V2 universal handoff contract

For every producer/receiver transfer, emit and validate `schemas/v4/handoff-envelope.schema.json` through the M00 V2 handoff procedure. Preserve this skill's public ID, trigger and domain ownership. Populate producer/recipient, case/project IDs, typed input/output artifact refs, decisions, inferences, assumptions, unknowns, conflicts, inherited constraints, trace links, acceptance checks and limitations. A JSON Schema PASS is structural only: semantic validation must resolve externally indexed artifacts, verify actual bytes/hashes, check producer identity from M00 dispatch context and confirm dependency status. Missing evidence remains `UNKNOWN`, `NOT_RUN` or `BLOCKED`; never manufacture PASS.

## V2 operating procedure

Follow `skills/health-evidence-safety-auditor/references/v2-operational-protocol.md` for claim extraction, evidence hierarchy, source snapshots, claim-to-source support, safe wording, counterevidence and human clinical escalation. S02 remains sole owner of Health Truth Registry and Fact Lock. Hash integrity, provenance, semantic support and clinical approval are distinct states.
