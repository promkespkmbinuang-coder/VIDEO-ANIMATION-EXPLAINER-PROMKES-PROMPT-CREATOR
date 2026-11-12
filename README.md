# Video Explainer Promkes — V4.0.0

**Architecture:** M00 + S01–S13 · **Governance:** Evidence-Contract-Gated Production Compiler · **Release:** private / public release HOLD

Sistem produksi explainer animasi promosi kesehatan yang menjaga integritas bukti kesehatan, kontinuitas kreatif, provenance, keamanan prompt, izin/hak, dan mutu artefak. V4 menambahkan validator kontrak yang dapat dijalankan dan gate G0–G7 yang fail-closed, sambil mempertahankan spesialisasi M00 + S01–S13.
**Architecture:** M00 + S01–S13 · **Target:** V4.0 · **Release posture:** private plugin / public release HOLD

Sistem produksi explainer animasi promosi kesehatan yang memisahkan klaim faktual, bukti, wording yang diizinkan, narasi, referensi visual, continuity, prompt, scene timing, manifest, renderer capability, QA artefak, aksesibilitas, dan persetujuan manusia. M00 mengoordinasikan spesialis S01–S13 tanpa menganggap spesialis sebagai agen runtime otomatis.

## What V4 adds

- JSON Schema Draft 2020-12 contracts for claim records and artifact envelopes.
- A Python CLI validator and eight sequential fail-closed gates with 21 executable controls.
- Claim-to-source provenance and snapshot hash checks; reviewer-matched, hash-bound approval records.
- Narrative claim traceability and exact safe-wording enforcement.
- Visual continuity/reference locks and untrusted-prompt boundary checks.
- Prompt-injection heuristic scan, frame arithmetic, manifest hash/path validation.
- Exact renderer/provider/version capability checks and evidenced static-code checks.
- Artifact hash checks, accessibility evidence and hash-bound release approval records.
- Dependency DAG validation, transitive invalidation planning, non-destructive invalidation application, approval invalidation and hash-bound revised snapshot output.
- Heuristic risk/applicability triage for the 1,000 candidate matrix; no control is auto-excluded or marked executed.
- Reproducible pytest suite and CI evidence artifacts.

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
python scripts/v4_gate_engine.py --help
python scripts/generate_v4_control_candidates.py --output build/control-candidates.json
python scripts/v4_control_risk_triage.py --input build/control-candidates.json --output build/control-risk-triage.json
python scripts/v4_gate_engine.py validate-claim --input claim.json
python scripts/v4_gate_engine.py validate-artifact --input artifact-envelope.json
python scripts/v4_gate_engine.py evaluate --project project.json --output build/gate-report.json
python scripts/v4_gate_engine.py evaluate --project project.json --require-release
python scripts/v4_gate_engine.py apply-invalidation --project project.json --changed SRC-001 --output build/project-invalidated.json
python scripts/v4_gate_engine.py invalidation-plan --project project.json --changed SRC-001
```

See [implementation and validation guide](docs/M00-V4.0-IMPLEMENTATION-AND-VALIDATION.md) and [architecture specification](docs/M00-V4.0-EVIDENCE-CONTRACT-GATED-PRODUCTION-COMPILER.md).

## Gate map

| Gate | Control boundary |
|---|---|
| G0 Intake | Input inventory, privacy, rights basis, byte-verifiable untrusted input |
| G1 Fact Lock | Claim schema/semantics, source provenance, evidence state, clinical reviewer approval |
| G2 Narrative | Claim-ID traceability and exact approved wording |
| G3 Visual | Canon lock and scene reference resolution |
| G4 Prompt | Instruction injection heuristics and trusted/untrusted boundary |
| G5 Manifest | Contiguous frame arithmetic, canonical hash and safe paths |
| G6 Code | Exact renderer capability record and evidenced static checks |
| G7 Release | Local artifact hash, accessibility QA evidence and release approval |

A downstream gate can pass only if every predecessor gate passes. NOT_RUN, NOT_VERIFIED, PARTIAL, BLOCKED, STALE and INVALIDATED are never promoted to PASS. NOT_APPLICABLE requires an explicit rationale.

## Control model: 1,000 candidates ≠ 1,000 tests

The generator enumerates 1,000 candidate IDs (10 domains × 10 gates × 10 test families). Enumeration does not execute controls. The executable implementation currently contains 21 named controls with deterministic tests. Future candidates need their own applicability decision, oracle, positive and negative test, evidence format, remediation and retest rule.

## Integrity and limitations

A PASS means only that a deterministic oracle accepted the supplied data/evidence. SHA-256 establishes byte identity, not factual truth, authority, licence or approval. Structural approval records do not authenticate a person's identity, credentials or cryptographic signature. Prompt scanning is heuristic. The engine checks local artifacts and supplied QA evidence; it does not decode or perceptually inspect MP4. Capability records do not execute Remotion. Live ChatGPT invocation, external AI/ASR/diarization, TTS, actual renderer integration/render, codec and media QA, accessibility user testing, institutional clinical/legal/privacy approvals and final human release decision remain separate.

## Repository status

PR #3 has been merged. Its first post-merge validation run revealed malformed plugin manifests. A follow-up corrective change is being prepared; CI must pass on the actual current head before describing this repository state as green. Public release remains HOLD. Repository visibility alone does not grant an open-source licence; publisher rights and licence decisions remain pending.

Private ChatGPT plugin: https://chatgpt.com/plugins/plugins_6af57525bfdc8191af0a262699b6df58

No open-source licence is granted by repository visibility alone. The publisher must verify ownership and explicitly decide the licence before public redistribution.
