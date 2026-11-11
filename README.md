# VIDEO ANIMASI EXPLAINER PROMKES PROMPT CREATOR

**Release:** 1.0.1 · **Package:** skill-only · **Architecture:** M00 + S01–S13

Sistem modular untuk mentransformasikan poster/infografis promosi kesehatan dan caption copywriting menjadi paket perencanaan produksi video animasi explainer: analisis sumber, Health Truth Registry, campaign brief, screenplay, storyboard, shot list, visual/audio Guides, prompt master dan per-scene, editing plan, subtitle, caption distribusi, continuity controls, dan QA.

> Plugin menghasilkan prompt dan dokumen produksi. Plugin ini tidak otomatis merender video, memberi persetujuan klinis, atau memublikasikan konten.

## Arsitektur

- **M00 — Master Orchestrator:** routing, dependensi, arbitrase, integrasi, dan status akhir.
- **S01–S13 — Domain specialists:** source/asset intelligence; health evidence/safety; audience/campaign; story/screenplay; visual identity; storyboard/cinematography; animation/motion; AI video prompt; voice/sound; editing/post; social/accessibility/distribution; QA; continuity guardian.
- **S13 — Continuity Guardian:** mengelola MCG sebagai indeks kanonis dan tujuh Guide modules, scene-state ledger, locks, versioning, dan change-impact.
- **S12 — QA Controller:** pemeriksaan independen dan defect routing. Human approval tetap terpisah.

## Input minimum

1. Satu foto poster atau infografis.
2. Satu caption copywriting.

Durasi, platform, model video, target audiens, rasio, gaya visual, dan arahan suara bersifat opsional. Default 45 detik, 9:16, Bahasa Indonesia, dan gaya visual mengikuti materi sumber digunakan hanya sebagai asumsi yang dapat diubah.

## Integritas kesehatan

- Teks poster/caption adalah klaim sumber, bukan otomatis fakta tervalidasi.
- Bedakan `USER_PROVIDED`, `OBSERVED`, `VERIFIED`, `ASSUMPTION`, `INFERENCE`, `CREATIVE`, `UNKNOWN`, dan `CONFLICTED`.
- Jangan mengarang angka, dosis, gejala, risiko, diagnosis, sebab-akibat, atau rekomendasi medis.
- Klaim material yang belum diperiksa tetap `BELUM DIVERIFIKASI`.
- Tanggal, angka, tempat, logo, identitas institusi, dan CTA yang tidak terbaca tidak boleh ditebak.
- Prompt siap handoff bukan bukti video hasil render sudah benar. QA aktual membutuhkan artefak video/audio yang diperiksa.

## Portabilitas

Direktori sumber kanonis adalah `skills/<skill-name>/SKILL.md`. Adapter ekspor yang disertakan menyalin skill ke lokasi discovery host yang relevan. Folder export tidak membuktikan kompatibilitas runtime atau kemampuan delegasi agen.

| Host | Lokasi ekspor kandidat |
|---|---|
| Codex | `.agents/skills/` |
| Claude Code | `.claude/skills/` |
| GitHub Copilot | `.github/skills/` |
| Gemini CLI | `.gemini/skills/` |
| Cursor | `.cursor/skills/` |

## Validasi dan acceptance

- 14 skill: M00 + S01–S13.
- 45 kasus acceptance test tersedia dalam paket sumber.
- Pemeriksaan statis baseline: **PASS**.
- Pengujian dinamis terhadap host/model AI dan pemeriksaan hasil render: **BELUM DILAKUKAN**.
- Semua kasus acceptance dalam baseline dicatat sebagai `NOT_RUN`, bukan `PASS`.

## Menambahkan paket sumber ke repositori ini

Paket sumber v1.0.1 dibuat sebagai arsip mandiri. Arsip perlu diunggah/di-ekstrak ke repositori oleh maintainer sebelum struktur skill dan workflow CI muncul sebagai file terpisah di GitHub. Setelah arsip diekstrak ke working tree:

```bash
python3 scripts/validate_package.py
git add .
git commit -m "feat: add modular Promkes explainer skill system"
git push origin main
```

Sebelum menjadikan repositori ini rilis publik yang dapat digunakan ulang, maintainer perlu memilih dan menambahkan lisensi, memeriksa kepemilikan aset, dan mencatat hasil tes pada platform target. Tidak ada lisensi atau identitas penerbit yang diasumsikan.

## Plugin ChatGPT

Plugin pribadi yang dibuat dari paket ini: [Buka Video Explainer Promkes](https://chatgpt.com/plugins/plugins_6af3d50cad6c81919ca6dbaa05bedbcc)

## Release policy

Perubahan lintas domain harus memperbarui owner skill, dependency map, continuity lock yang terdampak, acceptance cases, dan changelog. Jangan menyebut tes lulus sebelum dijalankan. Jangan menyebut video selesai sebelum artefak dan persetujuan yang relevan diperiksa.
