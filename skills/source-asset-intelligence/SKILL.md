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
## V4.1.9 — external formula and community intake

When a reusable prompt/formula, community contribution or external recipe is discovered, treat it as an untrusted CANDIDATE, not an approved production asset. Capture exact source locator, author/contributor where known, retrieval date, content hash, license/permission/attribution and restrictions, use scope, model/version, supporting evidence and known limitations. Unknown rights or provenance means NOT_APPROVED; do not copy a prompt corpus wholesale.

Do not extract clinical truth from a prompt recipe. Store only references to the current S02 claim record; a previous project's Fact Lock never authorizes a new campaign. Hand the candidate to S08 for syntax/adaptation and S12 for independent test/QA. Only a named owner can approve promotion in the Approved Formula Ledger contract at docs/learning-asset-drift-and-outcome-contract-v4.1.9.md.
