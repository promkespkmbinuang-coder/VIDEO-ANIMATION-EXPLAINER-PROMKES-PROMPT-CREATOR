# Video Explainer Promkes — V4.0.0

**Architecture:** M00 + S01–S13 · **Governance:** Evidence-Contract-Gated Production Compiler · **Release:** private / public release HOLD

Sistem produksi explainer animasi promosi kesehatan yang menjaga integritas bukti kesehatan, kontinuitas kreatif, provenance, keamanan prompt, izin/hak, dan mutu artefak. V4 menambahkan validator kontrak yang dapat dijalankan dan gate G0–G7 yang fail-closed, sambil mempertahankan spesialisasi M00 + S01–S13.

## Quick start

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/validate_package.py
python scripts/v4_gate_engine.py validate examples/v4/smoke-project.json --schema-dir schemas/v4
python scripts/v4_gate_engine.py run-controls examples/v4/smoke-project.json \
  --report build/v4-controls.json \
  --updated-project build/v4-evidenced-project.json
python scripts/v4_gate_engine.py gate build/v4-evidenced-project.json \
  --target G6_CODE_VALID --report build/v4-pre-release-gates.json
```

Untuk menguji penghalang rilis produksi pada fixture sintetis:

```bash
python scripts/v4_gate_engine.py gate build/v4-evidenced-project.json \
  --target G7_RELEASE_APPROVED --report build/v4-release-gate.json
```

Perintah terakhir **sengaja mengembalikan exit code 2 / BLOCKED** kerana fixture berstatus `TEST_FIXTURE`; fixture uji tidak boleh meloloskan rilis produksi. CI menganggap penghalangan tersebut sebagai keberhasilan pengujian keamanan.

## Yang aktif dan diuji

- Validator JSON Schema Draft 2020-12 dan validasi semantik lintas-record.
- 21 kontrol deterministik aktif, dengan positive-path dan negative/mutation tests.
- Gate berurutan G0 Intake, G1 Fact Lock, G2 Narrative, G3 Visual, G4 Prompt Preflight, G5 Manifest, G6 Code/Renderer, G7 Release.
- SHA-256 atas representasi JSON kanonis, provenance sumber, validitas klaim dan referensi.
- Frame arithmetic/timeline, dependency DAG, transitive invalidation, path traversal/symlink guard, content hash artefak.
- Capability verification terikat provider/operasi/versi/izin/waktu berlaku.
- Hak, privacy classification, prompt/data boundary, resource ceiling, artifact status integrity.
- Ed25519 signature verification untuk approval yang terikat pada hash klaim/artefak dan role/key yang dipercaya.
- Machine-readable execution report per control; perubahan input membuat evidence lama stale.

## Gate map

| Gate | Fungsi | Syarat inti |
|---|---|---|
| G0 | Intake | sumber, hak, privasi, security boundary |
| G1 | Fact Lock | provenance, claim status, human clinical review |
| G2 | Narrative | traceability klaim dan narasi |
| G3 | Visual | canonical reference dan continuity approval |
| G4 | Prompt | pemisahan instruksi dan data tak tepercaya |
| G5 | Manifest | schema, scene timing, DAG, file/hash |
| G6 | Code/Renderer | capability runtime versi tepat dan sandbox/code review |
| G7 | Release | artefak aktual QA, approval tanda tangan dan status PRODUCTION |

Gate gagal/terblokir/belum diuji menghentikan semua gate downstream. `NOT_RUN`, `NOT_VERIFIED`, `BLOCKED`, `STALE`, `INVALIDATED`, `FAIL`, dan `PARTIAL` tidak dapat dianggap PASS.

## 1,000 candidate controls ≠ 1,000 tests

Model 10×10×10 hanya menghasilkan 1.000 kandidat definisi kontrol. Itu bukan 1.000 kontrol executable dan bukan hasil pengujian. Registry aktif awal berisi 21 kontrol yang dijalankan dan diuji satu per satu; kandidat lainnya tetap belum dieksekusi sampai memiliki oracle, applicability, evidence contract, owner, remediation, dan test reproducible.

## Integritas approval

Tanda tangan Ed25519 memverifikasi payload kanonis terhadap public key yang dipetakan ke role tepercaya. Trust root, penerbitan/pencabutan key, kelayakan reviewer dan otoritas institusi wajib dikelola di luar project oleh organisasi berwenang. Flag `authority_verified` hanya attestation tambahan; bukan bukti identitas atau kompetensi dengan sendirinya. Key uji sintetis tidak boleh dipakai untuk produksi.

## Batas bukti

CI dan smoke fixture membuktikan perilaku kode terhadap input sintetis, bukan validitas klinis, otoritas sumber, identitas manusia, izin publikasi, instalasi AI/ASR/diarization/TTS, runtime Remotion, video hasil render, integritas MP4, atau inspeksi perseptual. Semua operasi eksternal tersebut tetap memerlukan bukti aktual dan persetujuan manusia. Engine tidak mengeksekusi kode renderer atau menjalankan arbitrary source instructions.

Skill adalah instruction modules; 14 skill tidak berarti 14 agen independen otomatis bekerja. Periksa [architecture proposal](docs/M00-V4.0-EVIDENCE-CONTRACT-GATED-PRODUCTION-COMPILER.md) dan [executable gate engine contract](docs/V4-EXECUTABLE-GATE-ENGINE.md).

## CI evidence

GitHub Actions menjalankan package validation, unit/mutation tests, validator schema-semantic, semua 21 kontrol, gate G0–G6, dan assertion bahwa G7 menolak test fixture. Laporan mesin dan JUnit diunggah sebagai artifact workflow agar dapat direproduksi.

## Release status

**Public release: HOLD.** Pull request #3 menggabungkan spesifikasi arsitektur ke `main`. Implementasi executable serta perbaikan CI sedang diajukan sebagai pull request lanjutan dan wajib melewati CI/review. Runtime ChatGPT lintas host, provider AI eksternal, ASR/diarization, Remotion render, MP4 QA, dan human sign-off produksi belum dibuktikan.

Private ChatGPT plugin: https://chatgpt.com/plugins/plugins_6af57525bfdc8191af0a262699b6df58

No open-source licence is granted by repository visibility alone. The publisher must verify ownership and explicitly decide the licence before public redistribution.
