# VIDEO EXPLAINER PROMKES — HEALTH-FIRST PRODUCTION SYSTEM

**Version:** 1.2.2 · **Package:** skill-only · **Output:** Prompt-to-Reference · **Architecture:** M00 + S01–S13

Mengubah poster/infografis promosi kesehatan dan caption menjadi paket referensi produksi: still/reference prompts, storyboard, motion/timing references, audio/overlay/subtitle data, Reference Asset Manifest, dan renderer-neutral composition handoff untuk diproses kemudian dalam Remotion atau sistem sejenis.

> Plugin ini tidak menghasilkan prompt text-to-video, kode Remotion, atau file video final secara default. Render dan artefak video adalah proses downstream yang memerlukan implementasi dan QA tersendiri.
**Version:** 2.0.0 · **Architecture:** M00 + S01–S13 · **Delivery:** capability-gated, from blueprint to verified media.

Video Explainer Promkes 2.0 mempertahankan spesialisasi promosi kesehatan dan memperluas alur produksi dengan kemampuan audio intelligence, transcript/timing provenance, subtitle SRT/VTT, audio post, project manifest terpusat, render/export bersyarat, serta QA media aktual.

## Apa yang berubah pada V2

- Input tidak lagi hanya poster + caption. Sistem mendukung `POSTER_FIRST`, `AUDIO_FIRST`, `HYBRID`, dan `SCRIPT_FIRST`.
- S09 diperkuat menjadi **Audio Intelligence, Voice & Sound Production**: inspeksi audio, metadata, transkrip, pembandingan transcript, speaker/segment IDs, timing granularity, uncertainty, subtitle SRT/VTT, sound cue, dan mix specification.
- S10 diperkuat menjadi **Composition, Renderer Integration, Render & Export**: renderer readiness, adapter contract, proof render, full render, export, troubleshooting dan file verification saat runtime benar-benar tersedia.
- S12 menjadi **Dual-Layer QA**: QA konten/reference dan QA artefak media aktual. Hasil yang tidak diperiksa tetap `NOT_VERIFIED` atau `NOT_RUN`.
- Project Manifest V2 menyatukan fakta kesehatan, audio, MCG, scene, reference assets, motion, subtitle, sound, render, QA, distribution dan delivery.
- Targeted correction loop menginvalidasi hanya dependensi yang terdampak; perubahan sumber tidak boleh diam-diam mengubah fakta kesehatan atau canon karakter.

- **M00 — Master Orchestrator:** routing, dependensi, arbitrase, integrasi, dan status akhir.
- **S01–S13 — Domain specialists:** source/asset; health evidence; campaign strategy; story; visual identity; storyboard; motion references; still/reference prompt engineering; voice/sound; renderer-neutral handoff; accessibility/distribution; QA; continuity guardian.
- **S13 — Continuity Guardian:** MCG sebagai indeks kanonis, tujuh Guide modules, scene-state ledger, locks, versioning dan change impact.
- **S12 — QA Controller:** validasi independen, traceability, defect routing dan release gates. Human approval tetap terpisah.

Skill adalah modul instruksi yang dapat dipanggil host, bukan klaim bahwa 14 agen independen otomatis berjalan.
## Yang tidak berubah dan tidak boleh dilemahkan

1. S02 tetap pemilik tunggal Health Truth Registry, klaim kesehatan, evidence, safe wording dan Fact Lock.
2. S03 tetap pemilik tujuan kampanye, audience, behavior objective dan CTA.
3. S13 tetap pemilik MCG, tujuh Guide modules, canonical locks dan scene continuity.
4. S12 tetap independen dari penulis artefak; QA tidak boleh meluluskan hasil yang belum diperiksa.
5. Otoritas klinis/institusional dan izin publikasi tetap pada manusia yang berwenang.

1. Satu poster/infografis promosi kesehatan.
2. Satu caption copywriting.

Durasi, platform, renderer, target audiens, rasio, gaya visual dan arahan suara bersifat opsional; default harus diberi label dan dapat diubah.
## Input modes

| Mode | Input awal | Routing |
|---|---|---|
| `POSTER_FIRST` | Poster/infografis + caption | Source → Health Truth → Campaign → Story → Visual → Audio/Render |
| `AUDIO_FIRST` | Voice-over/audio dan/atau transkrip | Audio Intelligence → Health Truth → Campaign/Story → Visual → Render |
| `HYBRID` | Poster + caption + audio/transkrip | Source dan Audio intake dapat berjalan terpisah; konflik disatukan sebelum fact lock |
| `SCRIPT_FIRST` | Naskah/transkrip tanpa audio | Story/Health Truth; timing tetap `none` atau `estimated` sampai ada bukti audio |

Input yang tidak lengkap menghasilkan paket parsial dengan gap yang dinyatakan, bukan fakta yang ditebak.

- Teks poster/caption merupakan klaim sumber, bukan otomatis fakta tervalidasi.
- Bedakan `USER_PROVIDED`, `OBSERVED`, `VERIFIED`, `ASSUMPTION`, `INFERENCE`, `CREATIVE`, `UNKNOWN` dan `CONFLICTED`.
- Jangan mengarang angka, dosis, gejala, risiko, diagnosis, sebab-akibat atau rekomendasi medis.
- Klaim material yang belum diperiksa tetap `BELUM DIVERIFIKASI`.
- Tanggal, angka, tempat, logo, identitas institusi dan CTA yang tidak terbaca tidak boleh ditebak.
## Tingkat delivery

- `BLUEPRINT_ONLY` — konsep, naskah, reference atau spesifikasi awal; belum ada paket render yang cukup.
- `REFERENCE_READY` — reference package dan manifest telah memenuhi acceptance yang relevan.
- `RENDER_READY` — project/adapter package siap dijalankan; belum ada MP4.
- `RENDERED_PARTIALLY_VERIFIED` — file hasil ada, sebagian pemeriksaan belum dapat dilakukan.
- `RENDERED_VERIFIED` — file aktual ada, dapat dibuka, metadata/streams dan pemeriksaan media yang diwajibkan telah diperiksa dengan bukti.
- `BLOCKED` — kendala material pada sumber, kesehatan, izin, aset, kemampuan atau runtime.

`skills/<skill-name>/SKILL.md` adalah sumber kanonis. `scripts/export_platforms.py` membuat salinan tata letak untuk Codex, Claude, Copilot, Gemini dan Cursor. Ekspor folder tidak membuktikan instalasi, discovery, invocation atau runtime berhasil. Lihat [kebijakan kompatibilitas](docs/platform-compatibility.md).
Status delivery teknis bukan persetujuan klinis atau izin publikasi.

## Batas kemampuan dan integritas

- Skill adalah instruction modules, bukan bukti bahwa agen, ASR, diarization, TTS, image generator, editor, renderer atau cloud service telah tersedia.
- Setiap operasi harus diperiksa terpisah: audio decode, metadata, ASR, alignment, diarization, audio processing, image/reference generation, code/runtime, rendering, export dan media inspection.
- Timestamp hanya dianggap `word`/`phrase`/`segment` bila diberikan oleh sumber/tool yang benar-benar mendukungnya. Perkiraan harus dilabeli `estimated`.
- `PROMPT`, `REFERENCE`, `GENERATED_ASSET`, `SELECTED_ASSET`, `APPROVED_ASSET`, `RENDERED_FILE` adalah status berbeda.
- Tidak ada jaminan viral, FYP, hasil klinis, konsistensi karakter sempurna, atau zero hallucination.

- 14 skill: M00 + S01–S13.
- 7 Guide modules tercatat dalam arsitektur kontinuitas.
- 45 baseline acceptance cases + 13 Prompt-to-Reference cases = 58 spesifikasi uji.
- Semua kasus tetap `NOT_RUN` sampai oracle diuji dengan evidence.
- Validator statis: `python -m pip install -r requirements-dev.txt && python scripts/validate_package.py`.
- CI memvalidasi YAML strict, kedua manifest, nama folder/skill, local Markdown references dan traceability matrix.
- Workflow link-check memeriksa tautan Markdown eksternal.

Pemeriksaan statis bukan bukti runtime AI, validitas klinis, renderer integration, atau mutu video/audio.

## Status rilis

**HOLD untuk distribusi publik lintas platform.** Source paket diarahkan ke branch review GitHub. Keputusan lisensi belum dibuat oleh publisher, dan runtime lima host, model referensi eksternal, renderer, QA artefak serta human approval belum memiliki bukti eksekusi. Baca [audit remediation record](docs/audit-remediation.md) dan [GitHub release governance](docs/github-publication.md).

## Hak dan penggunaan

Tidak ada lisensi open-source yang diberikan pada versi ini. Publikasi repository tidak dengan sendirinya memberi hak untuk menggunakan ulang, memodifikasi atau mendistribusikan. Publisher harus memeriksa kepemilikan dan menentukan lisensi sebelum merilis.

## Plugin ChatGPT

[Buka Video Explainer Promkes](https://chatgpt.com/plugins/plugins_6af3d50cad6c81919ca6dbaa05bedbcc)
## Package validation

Validator statis V1 tetap memeriksa struktur inti M00 + S01–S13 dan 58 kasus baseline/reference. V2 menambahkan spesifikasi uji produksi di `tests/v2-production-cases.json`; kasus tersebut berstatus `SPECIFICATION_ONLY_NOT_RUN` sampai benar-benar dieksekusi. Static validation tidak membuktikan host runtime, ASR, renderer, media QA atau persetujuan manusia.


## M00 v4.0 architecture proposal

The repository now includes the **Evidence-Contract-Gated Production Compiler** specification at [docs/M00-V4.0-EVIDENCE-CONTRACT-GATED-PRODUCTION-COMPILER.md](docs/M00-V4.0-EVIDENCE-CONTRACT-GATED-PRODUCTION-COMPILER.md). It preserves M00 + S01–S13 and defines evidence contracts, state-transition gates, prompt-firewall controls, capability-based routing, human approval, change-impact invalidation and measurable QA.

**Important:** this is an architecture/implementation specification, not a claim that the plugin has already implemented all V4 controls. Candidate-control generation is not test execution. Runtime AI, live ChatGPT invocation, actual Remotion render and rendered-artifact QA remain separate evidence requirements. The plugin remains private and public release remains on HOLD.
