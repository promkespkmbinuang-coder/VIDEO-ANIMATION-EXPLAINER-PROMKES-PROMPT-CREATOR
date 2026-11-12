# Video Explainer Promkes — V4.1.2

**Architecture:** M00 + S01–S13 production specialists, with S14 as a cross-cutting context/release auditor. The GitHub editing-postproduction and private renderer-code-engineering S10 relationship remains a proposed mapping pending owner confirmation; retain both capabilities. **Production release:** HOLD pending external and human evidence.

Sistem produksi explainer animasi promosi kesehatan yang menerjemahkan poster/foto/infografis plus caption, audio/transkrip, naskah atau kombinasi sumber menjadi paket produksi yang dapat ditelusuri dari intake hingga QA.


The private Plugin Creator package additionally carries the executable-gate-engine operational helper; this is an intentional package-only support skill and is tracked separately from the 15 numbered GitHub modules. Exact binary/source parity is not claimed.

## Cakupan produksi

- Intake sumber, literal extraction, provenance, konflik, klasifikasi PII/hak dan untrusted-data boundary.
- Health Truth Registry, claim ledger, counterevidence, safe wording dan Fact Lock.
- Audience/campaign strategy, hook etis, pesan kunci, screenplay, VO dan CTA.
- Visual canon, MCG/Guides, storyboard/shot plan, still-reference prompt dan optional video prompt.
- Motion specification, audio intelligence, transcript/timing provenance, subtitle dan post-production.
- Renderer-neutral manifest, capability checks, adapter/handoff, artifact QA, accessibility dan release disposition.
- S14 cross-cutting preflight: conversation context register, source-to-requirement trace, release parity, change impact dan publication evidence.
- Package hygiene: duplicate-key JSON rejection, manifest/version parity, skill inventory dan cache-artifact rejection.

## Pengendalian konteks percakapan

S14 mengklasifikasikan item sebagai EXPLICIT, CONFIRMED_PREFERENCE, INFERRED, PROPOSED, UNKNOWN atau SUPERSEDED. Konteks historis hanya membuktikan bahwa permintaan/preferensi pernah disampaikan; bukan bukti kebenaran klinis, fakta kampanye terbaru, izin, identitas atau hasil tes.

Preferensi bahasa membumi, storytelling, hook yang menarik tetapi benar, nada tidak menggurui, pesan kunci dan CTA dapat menjadi voice-profile yang dapat diubah. Dialek Polewali Mandar atau sapaan brand “Halo Sola Seha’” hanya dipakai jika sesuai brief/brand profile dan ada contoh yang sahih. Jangan mengarang idiom lokal, stereotip atau fakta demografis.

DBD, TBC, fogging, tanggal, lokasi, statistik, institusi dan CTA dari satu kampanye bukan default global. Rasio 4:5 dan ruang logo pada poster statis tidak otomatis menjadi rasio video. Aspect ratio video, resolusi, platform, durasi, safe area, frame rate, bahasa, voice, renderer, model AI dan kebijakan audio tetap variabel per proyek.

## Gate dan batas klaim

Delapan gate berjalan berurutan dari intake sampai release approval. Engine memiliki 21 kontrol deterministik. Model 10×10×10 menghasilkan 1.000 kandidat definisi, bukan 1.000 tes yang sudah dieksekusi.

Hash membuktikan identitas byte, bukan kebenaran, kewenangan, lisensi atau persetujuan. Approval record struktural tidak mengautentikasi identitas/kompetensi manusia. Prompt-injection scan bersifat heuristik.

## Validasi lokal

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_package.py
python scripts/validate_release_consistency.py --root .
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
```

Validator release memeriksa strict JSON, manifest parity, SemVer, shortDescription maksimal 30 karakter, 15 skill utama, S14, dokumen versi, dan larangan cache/bytecode dalam paket. Ini tetap static validation, bukan runtime.

## Status bukti dan publikasi

- PR #13 merged pada 6aa128ebaa8d561fcedf7a52f027bd2a2a931198. Review independen tidak tercatat pada pemeriksaan audit.
- Tidak ada workflow run atau combined status yang terkonfirmasi pada merge commit PR #13; validasi main pada SHA itu NOT_VERIFIED.
- Private Plugin Creator V4.1.1 is verified by read-back (release `pluginrel_6af5d06d0c388191840a4861eadd953c`, discoverability PRIVATE). Important parity boundary: the private package still contains the legacy `CTRL-*` engine without `V4-CTL-*`, Ed25519 verification or the synthetic-fixture release guard. GitHub PR #14 contains a separate hardening candidate; it is not merged or synchronized into the private package. Do not treat its CI as validation of the private engine.
- Plugin save/read-back bukan bukti instalasi/invokasi ChatGPT.
- Remotion install pernah BLOCKED oleh npm DNS EAI_AGAIN; Studio, bundle, render dan MP4 QA tetap NOT_RUN sampai ada bukti baru.
- External AI video provider belum dipilih; clinical/legal/rights/privacy/brand/accessibility dan final human release approvals tetap NOT_VERIFIED/NOT_RUN.
- Tidak ada LICENSE yang ditambahkan. Repository visibility PUBLIC bukan lisensi open-source atau izin redistribusi.

Lihat docs/conversation-context-register-v4.1.2.json, docs/release-audit-v4.1.2.md dan docs/skill-source-parity-matrix.md untuk batas parity antar paket. Source publication, CI, host runtime, renderer/media QA, lisensi dan persetujuan manusia adalah status berbeda. **Production/public release tetap HOLD.**
