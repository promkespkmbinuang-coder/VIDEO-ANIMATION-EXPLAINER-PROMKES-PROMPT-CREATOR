# Video Explainer Promkes — Evidence-Gated Production System

**Architecture:** M00 + S01–S13 · **Target:** V4.0 · **Release posture:** private / public release HOLD

Sistem produksi explainer animasi promosi kesehatan yang memisahkan klaim faktual, bukti, wording yang diizinkan, narasi, referensi visual, continuity, prompt, scene timing, manifest, renderer capability, QA artefak, aksesibilitas, dan persetujuan manusia. M00 mengoordinasikan spesialis S01–S13 tanpa menganggap spesialis sebagai agen runtime otomatis.

## What V4 adds
- JSON Schema Draft 2020-12 contracts for claim records and artifact envelopes.
- A Python CLI validator and eight sequential fail-closed gates with 21 executable controls.
- Claim-to-source provenance and snapshot hash checks; hash-bound structural approval records.
- Narrative safe-wording/claim traceability; visual continuity/reference locks.
- Prompt-injection heuristic scan and explicit untrusted-input boundaries.
- Frame arithmetic, manifest hash/path validation, capability and static-code evidence checks.
- Artifact hash, accessibility evidence and release approval controls.
- Dependency DAG validation and transitive invalidation planning.
- Reproducible pytest suite and CI artifacts.
**Version:** 2.0.0 · **Architecture:** M00 + S01–S13 · **Delivery:** capability-gated, from blueprint to verified media.

## Quick start
Install requirements-dev.txt, then run python -m pytest -q.
Use python scripts/v4_gate_engine.py --help to inspect commands.
Evaluate with: python scripts/v4_gate_engine.py evaluate --project project.json --output build/gate-report.json
Add --require-release to return non-zero unless all eight gates pass.

See docs/M00-V4.0-IMPLEMENTATION-AND-VALIDATION.md and docs/M00-V4.0-EVIDENCE-CONTRACT-GATED-PRODUCTION-COMPILER.md.

## Gate map
| Stage | Gate | Decision boundary |
|---|---|---|
| L0 | G0 Intake | Inventory, privacy, rights, untrusted data |
| L1 | G1 Fact Lock | Claim schema, provenance, material claims, clinical reviewer evidence |
| L2 | G2 Narrative | Claim traceability and safe wording |
| L3 | G3 Visual | Continuity locks and reference resolution |
| L4 | G4 Prompt | Injection scan and prompt/data boundary |
| L5 | G5 Manifest | Timing, schema, hash and safe asset paths |
| L6 | G6 Code | Verified capability and static-check evidence |
| L7 | G7 Release | Artifact QA, accessibility evidence, release approval |

A failed/blocked/unrun predecessor prevents later stages from passing. NOT_APPLICABLE needs a reason. No automatic status promotion is allowed.

## 10×10×10 model is not a test result
The generator can enumerate 1,000 candidate IDs (10 domains × 10 gates × 10 test families). Those rows are planning candidates only. The current executable engine implements 21 named control IDs, tested through synthetic unit fixtures. It is incorrect to say 1,000 controls have passed or even been individually executed.

## Integrity and limitations
A PASS means only that the engine's stated deterministic oracle accepted the supplied data/evidence. Source snapshots, artifacts, schemas, command line, software versions and reports should be retained for replay. Structural human-approval checks do not independently authenticate identity, credentials or digital signatures. Prompt scanning is heuristic. Artifact QA checks file presence/hash and evidence references, not actual video decoding or perceptual media inspection. Live ChatGPT, external AI/ASR, Remotion runtime/render, MP4 QA, accessibility user testing and institutional approvals remain separate and require actual evidence.

## Status
The V4 code and validation suite are proposed through PR #3. Keep this PR in Draft until CI and reviews are complete. Public distribution remains HOLD. No open-source licence is granted by repository visibility alone; publisher must decide and verify rights before distribution.
- Input tidak lagi hanya poster + caption. Sistem mendukung `POSTER_FIRST`, `AUDIO_FIRST`, `HYBRID`, dan `SCRIPT_FIRST`.
- S09 diperkuat menjadi **Audio Intelligence, Voice & Sound Production**: inspeksi audio, metadata, transkrip, pembandingan transcript, speaker/segment IDs, timing granularity, uncertainty, subtitle SRT/VTT, sound cue, dan mix specification.
- S10 diperkuat menjadi **Composition, Renderer Integration, Render & Export**: renderer readiness, adapter contract, proof render, full render, export, troubleshooting dan file verification saat runtime benar-benar tersedia.
- S12 menjadi **Dual-Layer QA**: QA konten/reference dan QA artefak media aktual. Hasil yang tidak diperiksa tetap `NOT_VERIFIED` atau `NOT_RUN`.
- Project Manifest V2 menyatukan fakta kesehatan, audio, MCG, scene, reference assets, motion, subtitle, sound, render, QA, distribution dan delivery.
- Targeted correction loop menginvalidasi hanya dependensi yang terdampak; perubahan sumber tidak boleh diam-diam mengubah fakta kesehatan atau canon karakter.

## Yang tidak berubah dan tidak boleh dilemahkan

1. S02 tetap pemilik tunggal Health Truth Registry, klaim kesehatan, evidence, safe wording dan Fact Lock.
2. S03 tetap pemilik tujuan kampanye, audience, behavior objective dan CTA.
3. S13 tetap pemilik MCG, tujuh Guide modules, canonical locks dan scene continuity.
4. S12 tetap independen dari penulis artefak; QA tidak boleh meluluskan hasil yang belum diperiksa.
5. Otoritas klinis/institusional dan izin publikasi tetap pada manusia yang berwenang.

## Input modes

| Mode | Input awal | Routing |
|---|---|---|
| `POSTER_FIRST` | Poster/infografis + caption | Source → Health Truth → Campaign → Story → Visual → Audio/Render |
| `AUDIO_FIRST` | Voice-over/audio dan/atau transkrip | Audio Intelligence → Health Truth → Campaign/Story → Visual → Render |
| `HYBRID` | Poster + caption + audio/transkrip | Source dan Audio intake dapat berjalan terpisah; konflik disatukan sebelum fact lock |
| `SCRIPT_FIRST` | Naskah/transkrip tanpa audio | Story/Health Truth; timing tetap `none` atau `estimated` sampai ada bukti audio |

Input yang tidak lengkap menghasilkan paket parsial dengan gap yang dinyatakan, bukan fakta yang ditebak.

## Tingkat delivery

- `BLUEPRINT_ONLY` — konsep, naskah, reference atau spesifikasi awal; belum ada paket render yang cukup.
- `REFERENCE_READY` — reference package dan manifest telah memenuhi acceptance yang relevan.
- `RENDER_READY` — project/adapter package siap dijalankan; belum ada MP4.
- `RENDERED_PARTIALLY_VERIFIED` — file hasil ada, sebagian pemeriksaan belum dapat dilakukan.
- `RENDERED_VERIFIED` — file aktual ada, dapat dibuka, metadata/streams dan pemeriksaan media yang diwajibkan telah diperiksa dengan bukti.
- `BLOCKED` — kendala material pada sumber, kesehatan, izin, aset, kemampuan atau runtime.

Status delivery teknis bukan persetujuan klinis atau izin publikasi.

## Batas kemampuan dan integritas

- Skill adalah instruction modules, bukan bukti bahwa agen, ASR, diarization, TTS, image generator, editor, renderer atau cloud service telah tersedia.
- Setiap operasi harus diperiksa terpisah: audio decode, metadata, ASR, alignment, diarization, audio processing, image/reference generation, code/runtime, rendering, export dan media inspection.
- Timestamp hanya dianggap `word`/`phrase`/`segment` bila diberikan oleh sumber/tool yang benar-benar mendukungnya. Perkiraan harus dilabeli `estimated`.
- `PROMPT`, `REFERENCE`, `GENERATED_ASSET`, `SELECTED_ASSET`, `APPROVED_ASSET`, `RENDERED_FILE` adalah status berbeda.
- Tidak ada jaminan viral, FYP, hasil klinis, konsistensi karakter sempurna, atau zero hallucination.

## Package validation

Private ChatGPT plugin: https://chatgpt.com/plugins/plugins_6af57525bfdc8191af0a262699b6df58
