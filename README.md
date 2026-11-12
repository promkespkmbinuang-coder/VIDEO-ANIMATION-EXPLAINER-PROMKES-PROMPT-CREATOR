# VIDEO EXPLAINER PROMKES — HEALTH-FIRST PRODUCTION SYSTEM

**Version:** 2.0.0 · **Architecture:** M00 + S01–S13 · **Delivery:** capability-gated, from blueprint to verified media.

Video Explainer Promkes 2.0 mempertahankan spesialisasi promosi kesehatan dan memperluas alur produksi dengan kemampuan audio intelligence, transcript/timing provenance, subtitle SRT/VTT, audio post, project manifest terpusat, render/export bersyarat, serta QA media aktual.

## Apa yang berubah pada V2

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

Validator statis V1 tetap memeriksa struktur inti M00 + S01–S13 dan 58 kasus baseline/reference. V2 menambahkan spesifikasi uji produksi di `tests/v2-production-cases.json`; kasus tersebut berstatus `SPECIFICATION_ONLY_NOT_RUN` sampai benar-benar dieksekusi. Static validation tidak membuktikan host runtime, ASR, renderer, media QA atau persetujuan manusia.
