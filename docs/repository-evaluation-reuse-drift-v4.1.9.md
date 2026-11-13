
# Evaluasi arsitektur, reuse aset, drift eksternal dan tata kelola proporsional — V4.1.9

**Target:** promkespkmbinuang-coder/VIDEO-ANIMATION-EXPLAINER-PROMKES-PROMPT-CREATOR  
**Pembanding read-only:** cclank/lanshu-awesome-ai-video-kit  
**Baseline GitHub:** main, commit 2d469eee5069f21cd231c1b732c4359fd1ce3838, V4.1.8; diperiksa 13 November 2026.  
**Baseline Plugin Creator:** video-explainer-promkes-renderer-engine, V4.1.7, release pluginrel_6af6b60317608191874e58dee5dbba09, scope USER / PRIVATE.  
**Cakupan:** PARTIAL_WITH_DISCLOSED_BOUNDARY. Source yang dapat diakses, read-back plugin terpilih, PR dan ringkasan percakapan tersedia diperiksa; bukan seluruh raw conversation atau seluruh file biner.  
**Keputusan arsitektur:** evolusi aditif dan merger ke pemilik fungsi yang ada. Tidak menambah S15/S16 atau gate produksi baru.

## 1. Ringkasan eksekutif — tujuh temuan

1. **Akar inefisiensi bukan jumlah spesialis dan bukan evidence gate.** M00 + S01–S14 telah membagi domain produksi yang diperlukan. Bottleneck yang lebih mendasar adalah keberhasilan proyek belum menjadi reusable asset dengan provenance, status persetujuan, batas penggunaan, versi, dan bukti uji. Ini INFERENCE yang didukung oleh keberadaan schema/Guide/validator V4.1.8 tetapi tidak ditemukannya ledger formula terpadu pada inventory source yang diperiksa.
2. **PROMKES dan Lanshu berbeda spesies.** PROMKES adalah kompiler/kendali produksi Promkes berpagar bukti; Lanshu adalah knowledge kit prompt/model dengan kontribusi komunitas dan pemantauan sumber eksternal. PROMKES unggul pada S02, MCG, S12, S14, fail-closed dan traceability. Lanshu unggul pada aset prompt, metodologi, selector/translator dan monitoring eksternal.
3. **Lima usulan tidak membutuhkan lima skill baru.** AFL berada pada S01/S08/S12/S13; Drift Sentinel pada S08/S14; risk-proportional preflight pada M00/S14; Model Selection Advisor pada S08; Outcome Register pada M00/S12/S14. Yang diperlukan adalah kontrak data, lifecycle, review dan beberapa kemampuan pendukung, bukan pemilik otoritas baru.
4. **Drift Sentinel adalah satu-satunya usulan yang memerlukan kemampuan operasional terjadwal.** Skill tidak melakukan polling mingguan sendiri. Perlu workflow/script dan antrean review. Namun aktivasi belum aman sebelum endpoint resmi, baseline, permissions dan failure handling ditetapkan.
5. **Risk-proportional depth dapat mengurangi duplikasi tanpa menurunkan kontrol.** R0/R1 dapat mengurangi pengulangan metadata setelah pilot sah; R2 tetap full scrutiny; R3 stop/escalate. UNKNOWN minimal R2, highest-trust trigger wins, tidak ada average risk. S14 tetap mandatory untuk seluruh lane.
6. **Loop pembelajaran harus berbasis reuse yang dapat dibatalkan, bukan self-learning otomatis.** Formula hanya APPROVED setelah provenance, izin, scope, review S02 bila terkait klaim, QA S12 dan owner approval. Drift membuat evidence STALE/UNDER_REVIEW, bukan auto-approve model adapter.
7. **Status rilis harus dipisahkan.** GitHub main V4.1.8 dan plugin privat V4.1.7 belum parity. PR #23 merge; CI sukses pada head PR 050e0004b5373312dc7650baa3abaac3c6b6f5ad, tetapi review submissions independen kosong dan pemeriksaan status/run pada merge SHA main tidak mengembalikan status. Ini bukan bukti CI main gagal; artinya main CI NOT_VERIFIED dari pemeriksaan ini. Runtime eksternal, Remotion render, MP4 QA, pilot, rights dan persetujuan manusia tetap NOT_RUN / NOT_VERIFIED / HOLD sesuai domain.

## 2. Peta genetik repositori

| Sumbu | PROMKES | Lanshu | Implikasi |
|---|---|---|---|
| Kelas sistem | Health-first production control compiler | AI-video prompt knowledge kit | Tidak dapat dipertukarkan |
| Unit nilai | Project package, claim lock, beat/scene/motion, render handoff, QA evidence | Prompt, formula, model notes, methodology, contribution | PROMKES perlu memanen resep tanpa mengimpor klaim |
| Sumber kebenaran | S02 claim registry + source provenance + human authority | Official/reputable/community sources dengan tingkat provenance beragam | Formula eksternal tetap kandidat |
| Governance | M00, S02, S12, S13, S14 dan fail-closed | Kontribusi lebih ringan dan library update | Adopsi pola kontribusi, bukan tingkat kontrol |
| Model/provider | Exact model/version capability record; docs dan runtime terpisah | Selector capability matrix dan prompt translator | Perlu advisor berbukti, bukan hard-coded ranking |
| Drift | S08/S14 kontrak perubahan; belum ada sentinel PROMKES aktif yang tervalidasi | Workflow pemantauan berkala + hash baseline + issue | Adopsi deteksi; perbaiki lifecycle baseline |
| Reuse | Schema, examples, Guides dan prompt skills; belum ada approved formula lifecycle terpadu | Pustaka prompt dan cross-model matrix | AFL memberi leverage |
| Feedback | QA, release records dan kandidat KPI; baseline adopsi belum diukur | Community contribution/test video | Tambahkan outcome register minimum |

### Validasi hipotesis baseline

- Lanshu unggul pada pustaka formula/prompt, model selector, prompt translator, metodologi, template kontribusi dan endpoint monitoring: FACT dari tree serta file yang diperiksa.
- PROMKES unggul pada evidence gate, pemilik fungsi, MCG, claim/source trace dan status discipline: FACT dari skill, schema, gate engine, MCG, risk dan beat-sheet docs.
- PROMKES tertinggal pada reusable asset lifecycle, drift watch aktif, metric baseline dan formal community ingestion: FACT terbatas pada tidak ditemukannya implementasi/registry terkait di inventory source yang diperiksa; bukan bukti tidak ada proses informal di luar repo.
- Klaim volume Lanshu pada README diperlakukan sebagai deklarasi repo, bukan validasi seluruh isi, akurasi, lisensi atau runtime. Konten prompt tidak diimpor.

### Pola Lanshu: adopsi, adaptasi, penolakan

| Pola | Keputusan | Adaptasi |
|---|---|---|
| Prompt library + cross-model matrix | ADAPT | Registry aset dengan sumber, rights, model/version, scope, evidence dan status |
| Model selector | ADAPT | Advisor non-otoritatif; unknown ditampilkan |
| Prompt translator | ADAPT TERBATAS | Terjemahkan syntax, bukan makna/claim; factual change kembali ke S02 |
| Weekly endpoint monitor | ADAPT DENGAN KOREKSI | Candidate → triage → human review → accepted baseline; tidak auto-accept |
| Issue/template kontribusi | ADAPT | Intake dengan provenance, rights, test record dan S12 review |
| Hard-coded capability/rating | TOLAK | Tidak menjadi fakta tanpa bukti exact model/version |
| Salin prompt/formula tanpa izin | TOLAK | Tidak ada impor mentah; rights/attribution harus jelas |
| Ganti arsitektur PROMKES dengan Lanshu | TOLAK | Identitas evidence-gated compiler dipertahankan |

**Failure mode Lanshu yang teramati:** scripts/monitor_models.py menyimpan hash hasil crawl ke baseline sebelum workflow menyelesaikan pembuatan issue review. Jika issue creation gagal setelah baseline diperbarui, scan berikutnya berpotensi tidak mendeteksi perubahan yang sama. Hash halaman adalah sinyal perubahan, bukan bukti perubahan fitur atau persetujuan model. PROMKES tidak boleh menyalin urutan auto-commit baseline ini.

## 3. Matriks gap dan keputusan

| ID | Gap | Relevansi guardrail | Keputusan |
|---|---|---|---|
| GAP-01 | Belum ada approved formula lifecycle registry | Claim refs dan S02 tetap dijaga | ADAPT P1 |
| GAP-02 | Model choice tersebar di project/adapter discovery | Advisor tidak mengesahkan support | ADAPT P2 |
| GAP-03 | Prompt translation memerlukan semantic guard | Makna claim tidak boleh berubah | ADAPT P2, terbatas |
| GAP-04 | Tidak ada verified scheduled drift sentinel | Drift hanya menjadi candidate; no auto-approval | ADAPT P1 design, P2 activation |
| GAP-05 | Belum ada community formula intake formal | External source dianggap untrusted | ADAPT P1 |
| GAP-06 | Dokumentasi panjang dan beban UX | Kurangi duplicate capture, jangan hapus evidence | ADAPT setelah pilot |
| GAP-07 | Risiko hard-coded capability matrix | Exact provider/model/version required | TOLAK bila tanpa provenance |

## 4. Audit status operasional

| Capability | Status source | Status operasional/bukti | Dampak / bukti hilang |
|---|---|---|---|
| M00 + S01–S14 | PRESENT | HOST_RUNTIME NOT_VERIFIED | Skill contract bukan bukti invocation/handoff runtime |
| S02 Health Truth | PRESENT / single owner | Project-specific claim audit NOT_RUN pada evaluasi ini | Tidak ada campaign claims yang diaudit |
| S14 preflight | PRESENT / mandatory | Raw history coverage PARTIAL; host invocation NOT_VERIFIED | Tidak semua raw chat/file tersedia |
| MCG + 7 Guides + 3 protocols | PRESENT di GitHub tree | Live project continuity refresh NOT_RUN | Tidak ada project output untuk diuji |
| R0–R3 | Contract + validator + example PRESENT | Pilot PROPOSED / NOT_APPROVED; main SHA checks NOT_VERIFIED | Perlu adjudication, baseline dan sponsor |
| Beat-sheet trace | Schema + validator + example PRESENT | Live project integration NOT_RUN | Tidak ada live artifact chain |
| S07 motion contract | Schema + validator PRESENT | Renderer runtime mapping NOT_RUN | Schema bukan bukti motion dirender |
| S08 model adapter | Contract/schema PRESENT | Exact-model support UNKNOWN / NOT_CHECKED kecuali per adapter | Official docs feature/version dan runtime record belum disertakan |
| Remotion target | DESIGN_ONLY | Install/typecheck/bundle/render/MP4/S12 media QA NOT_RUN | Mapping bukan execution |
| S12 media QA | Criteria PRESENT | Actual rendered-media QA NOT_RUN | Tidak ada render artifact untuk inspeksi |
| Plugin ↔ GitHub parity | PARTIAL / NOT_SYNCED | Plugin private 4.1.7; GitHub main 4.1.8 | Different names/paths; private legacy CTRL vs GitHub V4-CTL |
| PR #23 | CLOSED / MERGED | PR-head CI success; review submissions kosong | Merge SHA main belum punya status/run terverifikasi |
| GitHub main CI | Workflow PRESENT | NOT_VERIFIED pada merge SHA | Combined status dan workflow-run retrieval kosong |
| GitHub scenario acceptance | 76 cases mapped | NOT_RUN | Case oracle individual belum dieksekusi |
| Private plugin acceptance | 20-case suite present | NOT_RUN | Bukan substitusi pytest atau GitHub suite |
| Drift Sentinel | No verified PROMKES scheduler/endpoint registry found | NOT_IMPLEMENTED / NOT_RUN | Perlu official allowlist, safe fetcher, review queue |
| Approved Formula Ledger | No canonical lifecycle registry found | NOT_IMPLEMENTED | Belum ada curated asset lifecycle |
| Model Selection Advisor | S08 foundation exists | NOT_IMPLEMENTED sebagai explicit advisor contract | Perlu feature evidence dan unknowns |
| Project Outcome Register | Metric definitions partly present | NOT_MEASURED / NOT_IMPLEMENTED | Belum ada baseline representatif |
| Clinical/legal/rights/privacy/brand/accessibility | Governance specified | NOT_RUN / NOT_VERIFIED | Human authority/artifact-bound approvals absent |
| Production/public release | README says HOLD | HOLD | Gate wajib belum ditutup |

### CI dan review: interpretasi yang benar

- PR #23 merged ke main commit 2d469eee5069f21cd231c1b732c4359fd1ce3838.
- PR-head 050e0004b5373312dc7650baa3abaac3c6b6f5ad: validate-package SUCCESS run 43397100940 dan markdown-link-check SUCCESS run 43397101050.
- Review submissions yang dapat diambil: kosong. PR body meminta draft sampai independent review, namun PR akhirnya merged. Ini governance inconsistency, bukan review approval.
- Status/run retrieval pada merge SHA main tidak memberi bukti. Status: MAIN_CI_NOT_VERIFIED, bukan green atau red.

## 5. Analisis akar masalah

### RCA-01 — Knowledge bukan reusable governed asset
Keberhasilan tersimpan sebagai dokumen/prompt/project, tetapi belum ada record yang mengikat formula → source → rights → model/version → kondisi pakai → hasil uji → reviewer → status → expiry/invalidation. Akibatnya reuse sulit diukur, formula lama mudah dipakai pada model berbeda, dan sumber eksternal dapat tampak approved tanpa pemeriksaan.

### RCA-02 — External drift belum punya two-baseline lifecycle
Deteksi perubahan dan penerimaan perubahan belum dipisahkan sebagai observed candidate vs accepted baseline. Hash halaman tidak menjelaskan fitur yang berubah. Risiko: false positive dari UI/noise, false negative dari fetch error, atau silent acceptance dari baseline auto-update.

### RCA-03 — Governance cost berasal dari duplikasi, bukan gate esensial
Metadata direkam ulang; private/GitHub path/name mapping berbeda; acceptance inventories dan engine implementations terpisah; snapshots bisa tertinggal dari source aktif. Biaya: cognitive load, stale docs, parity ambiguity. Akar: project fact belum selalu dirujuk melalui stable ID/hash antar artefak. Menghapus S02/S12/S13/S14 hanya memindahkan risiko.

### RCA-04 — Closed-loop improvement belum terbentuk
Metrik didefinisikan tetapi tidak ada register proyek yang konsisten menyimpan denominator, window, lane, evidence dan limitations. Tanpa cohort sebanding, tidak dapat membuktikan reuse mempercepat kerja atau preflight menurunkan rework. Akar: tidak ada measurement contract untuk proses internal yang privacy-minimized.

## 6. Evaluasi lima usulan

### AFL-001 — Approved Formula Ledger
- **Severity:** Tinggi
- **Akar masalah:** formula tidak punya lifecycle provenance, scope, rights, tested version, reviewer dan stale status.
- **Rekomendasi:** P1; implementasi di S01/S08/S12/S13, bukan skill baru. S01 intake/provenance; S08 compile/adapt; S12 independent QA; S13 continuity dependencies; S02 tetap satu-satunya pemilik health truth.
- **Jenis:** Preventif + Evaluatif
- **Guardrail check:** LOLOS. Hanya APPROVED yang dapat direuse; claim evidence tidak diwariskan antar proyek; klaim saat ini tetap ke S02.
- **Effort/Dampak:** M/L
- **Dependency:** record contract, rights policy, exact model/version evidence, S12 oracle, asset IDs/hash, human owner approval.
- **Pilot:** 10–15 formula non-clinical yang punya source/rights jelas; mulai CANDIDATE/UNDER_REVIEW; shadow lookup dibanding cara manual; tidak masukkan prompt komunitas mentah.
- **Acceptance:** 100% record memiliki source, owner, status, scope, rights, model/version atau UNKNOWN, QA oracle dan invalidation triggers; hanya APPROVED yang tampil sebagai reusable; STALE/REVOKED tidak muncul sebagai active.
- **Risiko residual:** overgeneralization, license change, bias sampel, prompt injection.
- **Prioritas:** P1.

### MDS-001 — Model Drift Sentinel
- **Severity:** Tinggi
- **Akar masalah:** belum ada verified scheduled watch dan accepted-baseline lifecycle di PROMKES.
- **Rekomendasi:** P1 design / P2 activation. Scheduler hanya setelah official endpoint allowlist dan policy ada. Simpan observed digest terpisah dari accepted digest; drift creates event/issue, baseline hanya berubah melalui reviewer-authorized commit.
- **Jenis:** Preventif + Evaluatif
- **Guardrail check:** LOLOS dengan syarat. Drift tidak mengubah adapter menjadi DOCS_VERIFIED/RUNTIME_TESTED; S08 menilai fitur, S14 menelusuri provenance/release.
- **Effort/Dampak:** L/L
- **Dependency:** official endpoint registry, terms/source review, stable fetcher, full SHA-256, normalization, error/retry policy, issue template dan baseline owner.
- **Pilot:** 3–5 official docs endpoints yang disetujui; 4 siklus shadow; bandingkan diff manual; no auto-baseline.
- **Acceptance:** fetch/parse error tidak menulis baseline; event idempotent; observed snapshot immutable; accepted baseline hanya setelah review; DOCS_VERIFIED per fitur; runtime terpisah.
- **Risiko residual:** endpoint noise, rate limits, JS-only docs, provider tidak umumkan breaking change, terms berubah.
- **Prioritas:** P1 contract, P2 scheduler.

### RPF-001 — Risk-Proportional Preflight Depth
- **Severity:** Kritis bila salah; Tinggi sebagai leverage efisiensi
- **Akar masalah:** pemeriksaan berulang dan capture metadata ganda; belum ada baseline effort/time.
- **Rekomendasi:** P0; perjelas M00/S14. S14 selalu mandatory; yang bervariasi hanya kedalaman tambahan, bukan kehadiran preflight/gate.
- **Jenis:** Preventif + Mitigasi
- **Guardrail check:** LOLOS hanya dengan aturan keras: highest lane wins; critical trigger forces R3; UNKNOWN material risk >=R2; R2/R3 excluded dari fast-track; R0 perlu S02 NO_MATERIAL_HEALTH_CLAIM; S02/S12/rights/privacy/continuity/accessibility/human approval tetap sesuai applicability.
- **Effort/Dampak:** M/L
- **Dependency:** M00 risk record, S14 baseline preflight, existing R0–R3 contract, lane checklist, reviewer baseline dan rollback owner.
- **Pilot:** Phase 0 baseline; Phase 1 shadow recommendations dengan standard workflow tetap berlaku; Phase 2 hanya R0/R1 setelah sponsor tertulis, owner, S02/S12 concurrence, rights/privacy review, sample approval dan rollback readiness.
- **Acceptance:** 0 gate bypass, 0 UNKNOWN-to-R0, 0 critical averaging, 100% audit completeness; time/effort reduction hanya setelah cohort sebanding tanpa major/critical escape naik.
- **Risiko residual:** misclassification, hidden high-risk, small-sample bias.
- **Prioritas:** P0 contract; pilot tetap PROPOSED/inactive.

### MSA-001 — Model Selection Advisor non-otoritatif
- **Severity:** Sedang
- **Akar masalah:** kebutuhan project perlu dipetakan ke capability model terkini; marketing matrix bukan evidence.
- **Rekomendasi:** P2; merge ke S08. Maksimal 3 kandidat dengan fit matrix, trade-offs, unsupported controls, unknowns, evidence refs dan exact provider/model/version.
- **Jenis:** Preventif + Evaluatif
- **Guardrail check:** LOLOS. Tidak mengubah Health Truth, risk lane, gate atau approval; no auto-select.
- **Effort/Dampak:** S–M/M
- **Dependency:** adapter schema, official docs, runtime evidence for runtime claim, supplied project constraints.
- **Pilot:** 10 synthetic non-clinical briefs, compare with independent human reviewer, candidate-only outputs.
- **Acceptance:** setiap fitur critical ada source ref atau UNKNOWN; no unsupported support statement; user/project remains selector.
- **Risiko residual:** model changes post-review; region/access/cost differ by account.
- **Prioritas:** P2.

### POR-001 — Project Outcome Register minimal
- **Severity:** Sedang
- **Akar masalah:** metric definitions exist but there is no consistent project-local register with denominator/window/lane/evidence.
- **Rekomendasi:** P1; add privacy-minimized process register in M00/S12/S14. Only operational process metrics; no health-behavior or clinical-effect analytics.
- **Jenis:** Evaluatif + Preventif
- **Guardrail check:** LOLOS dengan batas. No audience health behavior collection, no clinical effect claim, no unsupplied analytics. Supplied/authorized analytics only when relevant.
- **Effort/Dampak:** S–M/M
- **Dependency:** metric dictionary, denominator/time window, privacy review, pseudonymous event IDs, owner and missingness policy.
- **Pilot:** 10–20 project records or all eligible small cohort; only cycle time, active reviewer minutes, rework, reuse, stale evidence, QA escapes, trace coverage and status.
- **Acceptance:** every metric has numerator, denominator, unit, period, cohort, evidence locator, owner, missingness and caveat; no patient/audience behavior fields; NOT_MEASURED visible.
- **Risiko residual:** denominator bias, self-report bias, small sample, identifying staff.
- **Prioritas:** P1.

## 7. Temuan tambahan

1. **PAR-001 — Private/GitHub identity and parity debt (Tinggi):** private plugin name, repo plugin name, skill paths, S10 alias dan gate engine berbeda. Jangan samakan source hanya karena version bump. Explicit mapping/owner confirmation diperlukan; parity tetap PARTIAL/NOT_SYNCED.
2. **REL-001 — Merge governance gap (Tinggi):** PR #23 body mensyaratkan independent review sebelum siap, tetapi PR merged dan review submissions kosong. Review tidak boleh diklaim retroaktif.
3. **CI-001 — Main evidence gap (Tinggi):** CI PR-head sukses bukan CI merge SHA main. Main checks tetap NOT_VERIFIED.
4. **DOC-001 — Version/document drift (Sedang):** plugin V4.1.7, GitHub V4.1.8, private M00 heading lama V4.0.9 sementara isinya memuat addendum baru. Version materialized views perlu dibanding manifest/source.
5. **ACC-001 — Test inventory boundary (Tinggi):** GitHub 76 scenario cases dan private 20 acceptance records berbeda dan belum dieksekusi. Pytest tidak menutup case acceptance.
6. **LIC-001 — External reuse rights (Tinggi):** tidak ada prompt/formula Lanshu diimpor. Sebelum mengimpor, review license, provenance, attribution, third-party rights dan asset permission.
7. **MET-001 — Metric conflation (Sedang):** jangan gabungkan quality, usage, speed dan safety menjadi satu skor. Zero critical escape tidak dapat dikompensasi oleh cycle time cepat.

## 8. Roadmap prioritas

### P0 — segera
1. Rekonsiliasi version dan source identity; pertahankan divergence yang disengaja.
2. Konsolidasikan metadata capture dan lane checklist di M00/S14; S14 tetap mandatory.
3. Tegaskan no-auto-promotion dan status distinctions; pisahkan PR CI, main CI, scenario suite dan runtime.
4. Tambahkan kontrak ledger/drift/outcome; jangan aktifkan scheduler/fast-track.

### P1 — pilot terbatas
1. AFL untuk non-clinical formulas dengan rights/provenance dan S12 review.
2. POR process baseline.
3. R0/R1 risk-routing shadow mode; actual fast-track only after written authorization.

### P2 — eksplorasi
1. Drift Sentinel scheduler setelah endpoint allowlist, owner, permissions and accepted-baseline workflow approved.
2. Model Selection Advisor setelah evidence cukup.
3. Prompt translator syntax-only dengan semantic diff; re-review S02 jika factual wording berubah.

**Dependensi:** S14 source/release preflight → record contracts → S01 intake/S08 compile → S12 QA → M00 outcome aggregation → shadow baseline → authorized pilot. Drift scheduler dan Advisor menunggu evidence readiness.

## 9. Rencana patch tingkat file

| File | Perubahan | Pemilik | Dependensi |
|---|---|---|---|
| skills/master-orchestrator/SKILL.md | Risk-proportional preflight; orchestration ledger, drift, advisor dan outcome | M00 | S14/S02/S08/S12 |
| skills/source-asset-intelligence/SKILL.md | Candidate intake untuk community/external formulas, provenance/rights | S01 | AFL contract |
| skills/ai-video-reference-engineering/SKILL.md | AFL, non-authoritative MSA, stale adapter handling | S08 | S01/adapter evidence |
| skills/quality-assurance-controller/SKILL.md | Independent formula QA, reproducibility, stale evidence | S12 | Candidate records/oracles |
| skills/conversation-release-audit/SKILL.md | Drift lifecycle, accepted baseline, outcome register, parity | S14 | M00/S08/S12 |
| docs/learning-asset-drift-and-outcome-contract-v4.1.9.md | Canonical contract lima usulan | M00/S14 | Role mapping |
| docs/repository-evaluation-reuse-drift-v4.1.9.md | Audit decision record ini | S14 | Evidence snapshot |
| docs/metrics-and-improvement.md | Reuse/drift/process metrics dengan denominator | S12/S14 | Outcome contract |
| README.md / CHANGELOG.md | Release summary, tetap HOLD | Maintainers | Artifacts |
| plugin.json / .codex-plugin/plugin.json | Version/descriptive metadata; preserve identity/defaultPrompt | Maintainers | Release consistency |
| CI/tests | No executable monitor or fast-track in this change; add deterministic validation when schemas implemented | Maintainers | P1 design review |

Tidak ada perubahan pada S02 ownership, mandatory S14, MCG topology, R0–R3 lane semantics, gate authority, acceptance case status atau production release state.

## 10. Metrik keberhasilan

| Metric | Definisi | Batas |
|---|---|---|
| Approved reuse ratio | Approved-ledger references reused / eligible formula lookups | Lookup bukan quality proof |
| Reuse acceptance | Reused formula accepted without material rework / reused formulas reviewed | Stratify task/model/version |
| Drift detection latency | Source change evidence → candidate event | Tidak membuktikan perubahan material |
| Stale evidence detection | Stale/unknown adapter records found / records reviewed | Laporkan denominator |
| Cycle time | Median/P90 intake-complete → S12 handoff | Pisahkan external wait dan lane |
| Reviewer effort | Active review minutes per project/role/lane | No user surveillance |
| Rework rate | Project reopened upstream / completed project | Classify root cause |
| Trace completeness | Resolved required links / applicable links | N/A needs reason |
| QA escape | Major/critical defects after S12 / inspected deliverables | Critical not averaged away |
| Risk misclassification | Independently adjudicated lane differs / adjudicated projects | R2/R3 outside fast-track |

Baseline NOT_MEASURED sampai cohort/window ditentukan. Jangan menetapkan target sebelum baseline representatif. Jangan mengukur outcome kesehatan, perilaku audiens atau engagement baru; no additional analytics unless supplied and authorized.

## 11. Risiko residual dan mitigasi

| Risiko | Kenapa residual | Mitigasi |
|---|---|---|
| Provider docs opaque | Fitur berubah tanpa changelog | UNKNOWN/STALE; manual verification; runtime separate |
| Drift false positive | HTML/UI/timestamp noise | Versioned normalization + human diff |
| Drift false negative | JS docs/access failure | Persist error event; never update accepted baseline |
| Formula overfit | Satu project/model tidak general | Scope limits + exact model/version + multi-case |
| Community rights | Provenance/permission unclear | Quarantine; no APPROVED state |
| Health claim contamination | Reuse transports old facts | S02 re-verifies current claims |
| Reviewer bottleneck | Human experts finite | Risk priority, not auto-approval |
| Parity drift | Private/public source differ | Path map, hashes, read-back |
| False confidence tests | Unit tests not host/runtime | Separate scenario/runtime/media/human evidence |
| KPI small-sample bias | Cohorts unlike | Stratify; report uncertainty/missingness |

## 12. Asumsi, bukti belum tersedia dan jawaban 8 pertanyaan

### Asumsi/batas bukti
- Raw full text seluruh histori dan binary files tidak tersedia; S14 coverage partial.
- Lanshu diperiksa read-only; tidak ada prompt/code imported; README assertions are not full content verification.
- Tidak ada live host, external AI/ASR/TTS, Remotion install/typecheck/bundle/render, MP4 inspection, real audience test, clinical/legal/rights review atau human release approval.
- Main CI exact merge SHA belum terverifikasi.
- No live pilot, baseline metrics or approved formula entries were created.

### Jawaban pertanyaan kritis
1. **Akar inefisiensi:** aset belum tersedimentasi + external drift lifecycle + outcome loop; berikutnya parity/status-document debt. Bukan kekurangan modul dan bukan evidence gate.
2. **Esensial M00 + S01–S14:** single owner, S02, S12 independent QA, S13 continuity, S14 mandatory preflight, M00 gate arbitration. Biaya berlebih ada pada duplicate metadata, manual snapshots dan path reconciliation—bukan gate keselamatan.
3. **Proyek menjadi akselerator:** hanya artefak dengan provenance, rights, model/version, scope, S12 oracle dan owner approval masuk ledger; version/hash; invalidasi bila sumber/model/claim berubah; re-check claim lewat S02.
4. **Deteksi drift:** official endpoints, immutable observed snapshots, diff + issue candidate, separate accepted baseline, reviewer decision; adapter STALE/UNKNOWN until docs verified; runtime requires actual run.
5. **Preflight proporsional:** S14 baseline always; extra depth by lane; R2 full, R3 stop/escalate; UNKNOWN >= R2; highest trigger wins; only duplicate clerical capture may be reduced.
6. **Pembelajaran komunitas:** candidate intake → provenance/license/right → test → S08 adaptation → S12 QA → owner acceptance; unverified source quarantined, no claim imported as fact.
7. **Pengukuran:** cycle time, reviewer effort, rework, accepted reuse ratio, stale detection/latency, trace completeness, misclassification dan QA escape; all with denominator/cohort/window. No behavioral-health analytics.
8. **Residual risks:** provider opacity, rights, overfit, human bottleneck, false positive/negative, parity drift and test overconfidence; manage through status, quarantine, independent review, rollback and human authority.

## Final disposition

**RECOMMENDATION: ADDITIVE MERGE INTO EXISTING FUNCTIONS. NO NEW SPECIALIST SKILL.** AFL dan POR membutuhkan typed records; MDS pada akhirnya membutuhkan scheduler tetapi tetap inactive sampai sumber/permission/baseline approved. Risk-Proportional Preflight adalah refinement M00/S14, bukan gate baru. Model Selection Advisor adalah fungsi bounded S08, bukan authority.

**Release status: HOLD.** Audit ini tidak mensertifikasi clinical truth, runtime, external model support, renderer execution, media quality, rights, accessibility, human approval atau production publication.
