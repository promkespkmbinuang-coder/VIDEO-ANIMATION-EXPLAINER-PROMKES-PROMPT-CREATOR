---
name: source-asset-intelligence
description: Use when menjadi pintu masuk materi. mengurai poster/infografis, caption, identitas institusi, teks, visual, dan aset menjadi source material dossier yang dapat ditelusuri.
---

# S01 — Input & Asset Intelligence

## Mission

Menjadi pintu masuk materi. Mengurai poster/infografis, caption, identitas institusi, teks, visual, dan aset menjadi Source Material Dossier yang dapat ditelusuri.

## Single ownership

**Owns:** Poster Visual Analyst; Text Extraction Analyst; Caption Deconstructor; Brand Identity Extractor; Asset Inventory Manager; Source Conflict Detector.

**Does not own:** Tidak menetapkan validitas medis, menentukan strategi final, atau menulis screenplay.

The named role is a functional task assignment, not a claim that the model has professional credentials. Work within the authority of this domain and preserve M00's integration role.

## Inputs

Poster/infografis dan caption; opsi: brand guide, asset file, target channel.

## Workflow

Inventaris aset; OCR/visual reading hanya jika capability tersedia; klasifikasi observasi/sumber; ekstraksi literal; pencatatan lokasi dan confidence yang dijelaskan.

## Required output

**Source Material Dossier.**

Include: Teks yang terbaca, visual hierarchy, logo/warna, identitas, CTA, informasi inti, wilayah tak terbaca, daftar konflik, asset refs.

## Acceptance criteria

Setiap angka/tanggal/lokasi/CTA literal dipertahankan; unreadable ditandai; tidak ada teks rekaan.

## Edge cases and recovery

Poster/caption hilang → partial intake; teks kabur → UNKNOWN; sumber bertentangan → CONFLICTED. Jangan menebak.

## Handoff contract

**Send to:** S02, S03, M00.

Every handoff includes: `case_id`, `skill_id`, `status` (`COMPLETE/PARTIAL/BLOCKED/NOT_APPLICABLE`), `input_refs`, `outputs`, `decisions`, `inferences`, `assumptions`, `unknowns`, `conflicts`, `inherited_constraints`, `trace_links`, `acceptance_checks`, `handoff_to`, and `limitations`. Keep IDs stable within the project. A handoff is a document contract, not evidence that another agent actually ran.

## Stop rules

Stop or mark the affected component `HOLD/BLOCKED` when a critical missing fact, authority, consent, capability or source conflict makes safe completion impossible. Continue only with safe partial work and visible limitations. Never hide a failure or silently overwrite another domain's decision.

## Supporting reference

For shared definitions and project-wide contracts, consult `../master-orchestrator/references/` where the host resolves relative paths. If cross-skill file reading is unavailable, follow this skill's local contract and pass the missing reference dependency to M00.


## V4.1.9 Approved Formula Ledger intake

S01 owns candidate formula intake, not approval. For each candidate capture immutable source locator/snapshot, source type, observation date, version/hash where available, provenance, rights-holder/permission basis, usage restrictions, intended task, audience context, language, exclusions and known failure modes. Label community material unverified until independently checked. Never copy Lanshu prompt text, data or methodology verbatim; its MIT file applies to its own repository, not PROMKES or third-party linked assets.

Create a DRAFT/CANDIDATE AFL record. S01 cannot mark it APPROVED, interpret health claims or transfer Fact Lock. Missing/unclear rights means UNKNOWN/RESTRICTED and blocks reuse/publication. Formula records store claim IDs as references only, never copied claim wording or clinical interpretation. Route candidate to S08 for fit assessment and S12 for independent QA; require authorized human approval bound to the exact formula content hash.
