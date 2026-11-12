# Video Explainer Promkes — V4.0.4

**Architecture:** M00 + S01–S14 (15 skill modules) · **Governance:** Evidence-Contract-Gated Production Compiler · **Production release:** HOLD pending external and human evidence.

Sistem produksi explainer animasi promosi kesehatan yang mengubah poster/foto/infografis plus caption, audio/transkrip, naskah, atau kombinasi sumber menjadi paket produksi yang dapat ditelusuri dari intake hingga QA. V4.0.4 mempertahankan delapan gate fail-closed dan 21 kontrol deterministik, serta menambahkan audit konteks percakapan dan konsistensi rilis.

## Cakupan produksi
- Intake sumber dan provenance, PII, rights, source conflicts dan untrusted-data boundary.
- Health Truth Registry, claim ledger, counterevidence, safe wording dan Fact Lock.
- Audience/campaign strategy, ethical hook, key message, screenplay, VO dan CTA.
- Visual canon, MCG/Guides, storyboard, shot plan, still-reference prompt dan optional video prompt.
- Motion specification, audio intelligence, transcript/timing provenance, subtitles dan post-production.
- Renderer-neutral manifest, capability checks, adapter/handoff, asset QA, accessibility dan release decision.
- S14 conversation context audit dan release-change traceability.

## Konteks percakapan: jangan kehilangan keputusan
S14 mengaudit konteks yang benar-benar tersedia dan menandai tiap item sebagai EXPLICIT, CONFIRMED_PREFERENCE, INFERRED, PROPOSED, UNKNOWN atau SUPERSEDED. Konteks gaya yang berulang—bahasa membumi, storytelling, hook yang menarik tetapi benar, nada tidak menggurui, pesan kunci dan CTA—dapat menjadi preferensi editable, bukan aturan wajib untuk semua kampanye. Dialek Polewali Mandar dan sapaan brand seperti “Halo Sola Seha’” hanya dipakai jika cocok dengan brief/brand profile dan didukung contoh; jangan mengarang idiom lokal.

Konteks kampanye tunggal seperti DBD, TBC, fogging, tanggal, statistik atau lokasi tidak boleh menjadi fakta global. Rasio 4:5 dan margin logo yang diminta untuk poster statis tidak otomatis menetapkan rasio video. Video ratio, platform, resolusi, safe area, frame rate, bahasa, voice, renderer dan model AI tetap merupakan variabel tiap proyek. Hook tidak boleh menyesatkan, memanipulasi ketakutan, menstigma atau memperkuat klaim medis.

## Gate dan kontrol
G0 Intake → G1 Fact Lock → G2 Narrative → G3 Visual → G4 Prompt Preflight → G5 Manifest → G6 Code/Renderer → G7 Release. Hanya 21 kontrol deterministik yang aktif pada engine yang dijelaskan dalam dokumen V4 saat ini. Model 10×10×10 menghasilkan 1.000 kandidat definisi, bukan 1.000 tes yang sudah dieksekusi.

## Validasi
```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/validate_package.py
python scripts/validate_release_consistency.py --root .
python scripts/v4_gate_engine.py --help
```

CI/tes sintetis hanya membuktikan perilaku pada oracle dan fixture yang dijalankan. Tidak membuktikan validitas klinis, otoritas reviewer, instalasi/invokasi ChatGPT, provider AI eksternal, ASR/TTS, Remotion runtime, render MP4, inspeksi perseptual, hak atau persetujuan institusi.

## Status bukti
PR #7 telah merged ke main melalui commit `11e9d0c746d11934eadf8caa50aa12550b8eceaa`. Dua workflow PR-head #94 sukses pada `ad8013ccfe4dbfa92a91cd4751cd0c30316bca27`; deskripsi PR mencatat 51 pytest passed. Ini bukti head PR sebelum merge, bukan workflow baru pada merge commit. Lihat `reports/VALIDATION-REPORT.md` dan `reports/release-status.json`.

Private Plugin Creator V4.0.4 telah disimpan dan dibaca kembali; source read-back bukan host installation. Plugin Management terakhir melaporkan `not_installed`, live invocation NOT_RUN. Remotion dependency install terakhir BLOCKED oleh npm DNS EAI_AGAIN; Studio, bundle, render dan Remotion MP4 QA NOT_RUN. AI video provider belum dipilih. Human clinical/legal/rights/privacy/brand/accessibility/release approvals belum terverifikasi.

## Source sync dan lisensi
Versi manifest yang sama tidak membuktikan source-tree parity. Repositori GitHub belum memiliki adapter Remotion dan asset pendamping yang ada di private plugin; implementasi gate-engine, schema dan sebagian skill juga perlu rekonsiliasi file-per-file. Status lengkap tetap NOT_RECONCILED. Tidak ada LICENSE yang ditambahkan: public repository visibility bukan lisensi open-source atau persetujuan redistribusi.
