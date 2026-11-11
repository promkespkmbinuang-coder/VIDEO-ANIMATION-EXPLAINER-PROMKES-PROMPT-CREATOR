# VIDEO ANIMASI EXPLAINER PROMKES PROMPT CREATOR

**Version:** 1.2.0 · **Package:** skill-only · **Output:** Prompt-to-Reference · **Architecture:** M00 + S01–S13

Mengubah poster/infografis promosi kesehatan dan caption menjadi paket referensi produksi: still/reference prompts, storyboard, motion/timing references, audio/overlay/subtitle data, Reference Asset Manifest, dan renderer-neutral composition handoff untuk diproses kemudian dalam Remotion atau sistem sejenis.

> Plugin ini tidak menghasilkan prompt text-to-video, kode Remotion, atau file video final secara default. Render dan artefak video adalah proses downstream yang memerlukan implementasi dan QA tersendiri.

## Arsitektur

- **M00 — Master Orchestrator:** routing, dependensi, arbitrase, integrasi, dan status akhir.
- **S01–S13 — Domain specialists:** source/asset; health evidence; campaign strategy; story; visual identity; storyboard; motion references; still/reference prompt engineering; voice/sound; renderer-neutral handoff; accessibility/distribution; QA; continuity guardian.
- **S13 — Continuity Guardian:** MCG sebagai indeks kanonis, tujuh Guide modules, scene-state ledger, locks, versioning dan change impact.
- **S12 — QA Controller:** validasi independen, traceability, defect routing dan release gates. Human approval tetap terpisah.

Skill adalah modul instruksi yang dapat dipanggil host, bukan klaim bahwa 14 agen independen otomatis berjalan.

## Input minimum

1. Satu poster/infografis promosi kesehatan.
2. Satu caption copywriting.

Durasi, platform, renderer, target audiens, rasio, gaya visual dan arahan suara bersifat opsional; default harus diberi label dan dapat diubah.

## Integritas kesehatan

- Teks poster/caption merupakan klaim sumber, bukan otomatis fakta tervalidasi.
- Bedakan `USER_PROVIDED`, `OBSERVED`, `VERIFIED`, `ASSUMPTION`, `INFERENCE`, `CREATIVE`, `UNKNOWN` dan `CONFLICTED`.
- Jangan mengarang angka, dosis, gejala, risiko, diagnosis, sebab-akibat atau rekomendasi medis.
- Klaim material yang belum diperiksa tetap `BELUM DIVERIFIKASI`.
- Tanggal, angka, tempat, logo, identitas institusi dan CTA yang tidak terbaca tidak boleh ditebak.

## Portabilitas

`skills/<skill-name>/SKILL.md` adalah sumber kanonis. `scripts/export_platforms.py` membuat salinan tata letak untuk Codex, Claude, Copilot, Gemini dan Cursor. Ekspor folder tidak membuktikan instalasi, discovery, invocation atau runtime berhasil. Lihat [kebijakan kompatibilitas](docs/platform-compatibility.md).

## Validasi dan acceptance

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
