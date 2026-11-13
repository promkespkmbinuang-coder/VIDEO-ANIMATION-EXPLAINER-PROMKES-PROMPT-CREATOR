# V4.1.7 — Evaluasi Repository: Motion, Prompt Sinematik, Adapter Platform dan Governance

**Repositori utama:** promkespkmbinuang-coder/VIDEO-ANIMATION-EXPLAINER-PROMKES-PROMPT-CREATOR  
**Pembanding:** jhh266205-maker/motion-design-prompt-generator  
**Baseline source:** GitHub main commit 772809311a79b71236fa882a35c7c6479ad13d03. Commit main berikutnya yang diperiksa adalah e12cf3b5930de3140e3eb0e99b9a676688c01043 (perubahan FUNDING.yml). Tree yang diperiksa berisi 190 entry.  
**Plugin privat baseline:** video-explainer-promkes-renderer-engine V4.1.6, release pluginrel_6af689ab80ec8191b75a08d97cd11241.  
**Cakupan:** inspeksi source read-only terhadap manifest, README, struktur, skill, schema, test, skrip, CI, MCG dan dokumen comparator. Runtime comparator, live ChatGPT, provider AI, renderer, MP4, legal/rights, klinis dan human approval tidak diuji dalam audit source ini.

## A. Verdict eksekutif

1. **Governance utama kuat dan harus dipertahankan.** Main sudah mempunyai M00 + S01–S13 + S14, delapan sequential production gates, claim/source/evidence records, fail-closed statuses, approval contracts, S12 independent QA dan S13 canonical MCG.
2. Comparator unggul di prompt engineering gerak yang langsung operasional: 9-slot anatomy, time-coded beat sheet, easing/duration values, camera vocabulary, platform prompt presets, negative constraints dan JSON motion spec.
3. Hipotesis “main tidak punya gerak kuantitatif” terlalu absolut. S07 telah menyebut frame/time range, transform, path, easing dan phase; scene schema telah memuat fps/timebase/frame boundaries dan motion refs. Kesenjangan sesungguhnya adalah belum ada normalized element-motion record schema dengan semantic validation.
4. Hipotesis “main tidak punya timecode/beat” juga terlalu absolut. Timing tersebar pada S06/S07/S09/S10. Yang belum ditemukan ialah satu kontrak beat sheet dengan trace end-to-end beat → shot → motion → audio → overlay → QA.
5. Hipotesis “tidak ada platform adapter” harus dibedakan. S08 mengizinkan optional video prompt blocks dan adapter setelah capability check; docs/platform-compatibility.md adalah portability untuk agent skill hosts, bukan AI video model dialect adapter. Yang belum ditemukan adalah registry model/version yang mencatat feature evidence, docs dan runtime test secara terpisah.
6. S15 tidak diperlukan. S06 sudah memiliki kamera/shot, S07 gerak, S08 prompt/adapter, S10 renderer mapping, S12 QA, S13 continuity, S14 audit/perubahan, M00 orchestrator. S15 berisiko menduplikasi otoritas dan menambah handoff, bukan menutup akar gap.
7. Fast-track tidak boleh bypass. Risk triage script saat ini hanya memeringkat 1.000 kandidat heuristik; kandidat tetap NEEDS_PROJECT_REVIEW, NOT_RUN dan NOT_VERIFIED. Itu bukan project-specific risk lane atau bukti bahwa kontrol berjalan.
8. Rekomendasi: **evolusi aditif + refactor dokumentasi terbatas**. Tambahkan contracts, validator, adapter evidence, cinematic QA rubric dan risk-proportional pilot. Jangan melemahkan S02, fail-closed, human approval atau audit trail.

## B. Peta kondisi saat ini

| Komponen | Fungsi | Status baseline | Bukti source | Catatan |
|---|---|---|---|---|
| M00 | Mode routing, capability readiness, dependencies, gates, delivery aggregation | ADA / KUAT | skills/master-orchestrator/SKILL.md | Pertahankan sebagai satu-satunya orchestrator |
| S02 | Health Truth Registry, evidence, safe wording, Fact Lock | ADA / KUAT | skills/health-evidence-safety-auditor/SKILL.md; schemas/v4/claim-record.schema.json | Otoritas klinis tidak dipindahkan ke prompt/motion |
| S06 | Storyboard, shot, camera, framing, scene timing | ADA / PARSIAL TERSTRUKTUR | skills/storyboard-cinematography/SKILL.md; schemas/v4/scene-record.schema.json | Camera plan ada; beat contract tunggal belum ditemukan |
| S07 | Motion choreography, state, easing, path, timing refs | ADA / PARSIAL | skills/animation-motion-design/SKILL.md | Detail masih tekstual/tersebar; schema motion-record belum ada di baseline |
| S08 | Still/reference prompts, optional video prompt, capability policy | ADA / PARSIAL | skills/ai-video-reference-engineering/SKILL.md | Still/video separation benar; model dialect evidence registry belum ada |
| S09 | Audio/transcript provenance, timing, VO, subtitle/SFX | ADA / KUAT | skills/voice-sound-design/SKILL.md | Source precision harus membatasi downstream timing |
| S10 | Editing, composition, renderer mapping, conditional render/export | ADA / KUAT SECARA KONTRAK | skills/editing-postproduction/SKILL.md; docs/remotion-handoff.md | Handoff renderer-neutral bukan native schema universal |
| S12 | Independent content/reference/media QA | ADA / KUAT DASAR | skills/quality-assurance-controller/SKILL.md | Cinematic oracle terukur belum granular |
| S13 | MCG, seven Guides, locks, continuity dependencies | ADA / KUAT | skills/continuity-guardian/SKILL.md; schemas/v4/mcg-manifest.schema.json | Tidak mengambil alih motion/camera |
| S14 | Context audit, change impact, source parity, publication evidence | ADA / KUAT | skills/conversation-release-audit/SKILL.md | Pemilik yang tepat untuk repository evaluation/change impact |
| Gate engine | Eight sequential gates, fail-closed states and approvals | ADA / KUAT | scripts/v4_gate_engine.py | Jangan membuat gate duplikat |
| Risk triage | 1,000 hypothetical candidate controls | ADA / HEURISTIK | scripts/v4_control_risk_triage.py; tests/test_v4_risk_triage.py | Bukan project risk assessment |
| Scene schema | Frame/timebase, claim/reference/motion refs | ADA / DASAR | schemas/v4/scene-record.schema.json | Bukan keyframe-level motion schema |
| Platform compatibility | Skill-host export/discovery policy | ADA / DOMAIN BERBEDA | docs/platform-compatibility.md | Tidak sama dengan model video dialect adapter |
| CI/tests | Static/package validation, pytest, release and gate fixtures | ADA / KUAT DASAR | .github/workflows/validate.yml; tests/ | Tidak membuktikan external model/render/media |
| Metrics | Test/release/compatibility reports | PARSIAL | reports/; docs/engine-parity-status.md | KPI adopsi, usability, cycle-time baseline belum terlihat |
| Private/GitHub parity | Private plugin and public source reconciliation | PARTIAL / NOT_SYNCED | docs/engine-parity-status.md; Plugin Creator read-back | Versi sama tidak membuktikan engine/source parity |

## C. Matriks celah vs comparator

| Fitur | Repo utama | Motion-Design | Severity | Bukti | Dampak | Akar masalah |
|---|---|---|---|---|---|---|
| Quantified motion | Frame/time, transform/path/easing ada tersebar; no dedicated record | Motion grammar, easing/spring/duration and JSON spec | HIGH | Main S07, scene schema; comparator SKILL.md, motion-grammar.md, spec.schema.json | Units/keyframes/phases dapat berbeda; renderer mapping kurang deterministik | Tidak ada kontrak data kanonis untuk element motion |
| Beat/timecode | Timing ada across S06/S07/S09/S10; beat handoff belum tunggal | Time-coded beat sheet and shot purpose | MEDIUM | Main S06/S07/S09/S10; comparator SKILL.md | Narrative-to-shot-to-motion/audio trace lemah | Timeline dipisah menurut ownership tanpa integrated beat contract |
| Prompt anatomy | Components/negative constraints ada, namun 9-slot video prompt checklist tak ditemukan | Explicit 9-slot anatomy and QA | MEDIUM | Main S08; comparator SKILL.md | Missing prompt fields tidak mudah terdeteksi | No video prompt completeness contract |
| Model dialect | S08 conditional adapters/capability policy | Presets for Sora/Veo/Kling/Seedance/Runway | HIGH | Main S08 and docs/platform-compatibility.md; comparator references/platform-presets.md | Repeated manual rewriting; risk stale/unverified parameter claims | Adapter evidence not stored as versioned record |
| Machine-readable output | Scene/claim/MCG schemas and renderer handoff exist | Dedicated JSON motion schema | HIGH | Main schemas/v4/scene-record.schema.json, docs/remotion-handoff.md; comparator assets/spec.schema.json | Mapping ambiguity/schema drift | Scene metadata and element motion data are distinct contracts |
| Cinematic QA | S12 general timing/readability/continuity QA | Prompt-level observable quality gate | MEDIUM | Main S12; comparator SKILL.md | Cinematic defect classification inconsistent | No single detailed motion/cinematic QA rubric |
| Fast-track | Sequential gates plus heuristic candidate triage | Lighter prompt workflow | HIGH for efficiency | Main risk triage and tests | Low-risk scope carries possible duplicate process | No operational risk lane with baseline/rollback |
| Metrics | Release/test reports | Direct install and smoke test, prompt workflow | MEDIUM | Main reports; comparator README/test | Adoption/reduced iterations cannot be proven | KPI dictionary and measurement plan not yet present |

Comparator is a specialist motion prompt generator, not a health production governance compiler. Its narrower governance scope is not automatically a flaw relative to its purpose.

## D. Root cause (5 Whys)

### D1. Motion data remains distributed
1. Why are frame/keyframe specifications inconsistent? They are described across S07 prose, scene refs and renderer handoffs.
2. Why not one schema? Scene schema covers scene-level timing/refs; no separate element-motion contract was defined.
3. Why was it not prioritized? Governance, health truth and continuity were the initial architecture's dominant risks.
4. Why now material? Multi-element work requires stable units, phases, frame ranges and renderer mapping.
5. Root cause: missing contract boundary between scene timing and element motion, not missing motion owner.

### D2. Platform adapters are not auditable artifacts
1. Why are prompt variants hard to reuse? S08 adapter checking is conditional and project-specific.
2. Why can't verification be reused? There is no exact model/version registry containing features, official docs and runtime evidence.
3. Why not reuse host compatibility table? It covers skill-host discovery, not video model behavior.
4. Why does it matter? Model/UI/API versions change supported controls and prompt dialect.
5. Root cause: capability evidence is not persisted as versioned adapter records.

### D3. Heavy low-risk workflow
1. Why do simple projects face many stages? Sequential gates were designed around high-impact health risks.
2. Why is no operational quick lane? Risk triage ranks theoretical candidates, not actual project risk.
3. Why not relax? False-negative classification rates are not measured.
4. Why can't efficiency be judged? Cycle-time/reviewer-effort/adoption baselines are not evident.
5. Root cause: risk-proportional workflow and efficiency measurement have not matured into a reversible pilot; fail-closed principles remain appropriate for high-risk content.

## E. Risiko jika tidak diperbaiki

| Risiko | Probabilitas | Dampak | Severity | Mitigasi |
|---|---|---|---|---|
| Ambiguitas frame/unit motion | Medium-high | High | HIGH | Canonical motion schema, half-open frame range and semantic validator |
| Adapter model usang/overclaim | High | High | CRITICAL | Exact model/version docs, feature evidence, runtime distinction, review trigger |
| Klaim kesehatan berubah saat prompt rewriting | Medium | Critical | CRITICAL | S02 locks, immutable overlays, negative constraints, S12 trace QA |
| Fast-track salah klasifikasi konten berisiko | Medium | Critical | CRITICAL | Unknown defaults protective; pilot, audit sample and rollback on escape |
| Renderer mapping silently loses timing/easing | Medium | High | HIGH | S10 mapping report and target-specific tests |
| S15 creates duplicate authority | Medium | Medium-high | HIGH | Do not add S15; use current single-owner chain |
| Static tests mistaken for render/media evidence | Medium | Critical | CRITICAL | Keep static/integration/render/media/human status separate |
| Private/GitHub parity drift | High | High | HIGH | S14 parity matrix, read-back; no engine sync without independent review |

## F. Roadmap aditif

### Quick wins — 0–2 minggu
- S07 motion schema, valid/invalid fixtures, semantic validator and edge tests. Files: schemas/v4, scripts/validate_motion_contract.py, tests/test_motion_contract.py. Acceptance: half-open duration arithmetic, keyframe/phase bounds, S09 source precision and S06 camera ownership validated.
- S08 nine-slot prompt completeness and exact model/version adapter schema. Acceptance: unknown stays NOT_CHECKED; docs vs runtime evidence split; every feature support claim has evidence refs.
- S12 cinematic QA criteria integrated into current QA/gates. Acceptance: every check has oracle, expected/observed state, evidence and defect owner; absent media NOT_RUN.
- R0–R3 routing policy published as proposal only. Acceptance: unknown risk escalates, no mandatory control bypass.

### Medium term — 1–2 bulan
- Beat-sheet contract linking approved message/claim, scene, shot, motion, audio, transition, overlay and QA. Acceptance: end-to-end trace and timing precision preserved.
- Implement one renderer adapter at a time. Acceptance: exact target/version integration test and proof artifact; other renderers NOT_TESTED.
- Controlled R0 pilot with measured baseline and standard-path comparator. Acceptance: no increase in health/rights/privacy/accessibility defects; rollback criteria exercised.
- KPI dictionary and privacy-minimized adoption/usability event definitions.

### Long term — 3–6 bulan
- Add 3–5 model adapters only when official documentation and actual test capability exist. Acceptance: exact model/version docs refs, feature map, runtime refs and recheck trigger.
- Cross-renderer conformance suite and measured mapping-loss report. Acceptance: unsupported controls never silently degrade.
- Periodic independent review of prompt quality, cinematic defects, adoption, cost and risk-lane calibration.

## G. Intervention design

| Intervensi | Mekanisme | Guardrail | Metrik | Audit |
|---|---|---|---|---|
| Motion contract | Normalize state/keyframe/path/easing/frame | Renderer-neutral; S06 camera ownership; S09 precision inherited | Schema validity, frame mismatch, mapping loss | CI positive/negative/edge, S12 |
| Platform adapter | Model/version dialect/capability record | Unknown default; official docs separate from runtime | DOCS_VERIFIED and RUNTIME_TESTED counts separately | Version-pinned fixture, evidence refs, S14 recheck |
| Cinematic QA | Observable beat/motion/readability/continuity checks | No subjective beauty score; no PASS without oracle | First-pass QA, defect escape, rework | S12 and actual artifact review |
| Risk route | Reduce duplicate work for low-risk tasks | No bypass evidence, S02, rights/privacy, S12 or human approval | Median/p90 cycle time and reviewer effort | Reversible pilot, comparison cohort, rollback |
| Metrics loop | Measure real adoption/quality | No vanity metrics; privacy minimization | Adoption, task success, iterations, cycle time, trace completeness | Baseline and periodic review |

## H. Prioritas Impact × Effort × Implementation Risk

| Prioritas | Intervensi | Impact | Effort | Risk | Keputusan |
|---|---|---|---|---|---|
| P0 | S07 motion schema + validator | High | Medium | Low-medium | First |
| P0 | S12 cinematic QA integration | High | Medium | Low | Merge into current QA |
| P0 | S08 adapter evidence schema | High | Medium | Medium | Build now; populate with evidence only |
| P1 | R0–R3 policy/pilot | High | Low-medium | High | Policy first; no bypass |
| P1 | S10 canonical-to-renderer mapping | High | High | Medium-high | Start with one renderer |
| P1 | S06 beat-sheet contract | Medium-high | Medium | Medium | After owner alignment |
| P2 | KPI/adoption baseline | Medium | Medium | Medium | After privacy review |
| P3 | S15 specialist | Low incremental | High | High | Reject; duplicates ownership |

## I. Metrik keberhasilan

No numerical target is asserted without baseline. Define and measure first.

- Low-risk cycle time: intake-complete to approved handoff; median/p90 by risk lane.
- Prompt iteration count: substantive revisions before static acceptance.
- First-pass QA acceptance paired with downstream defect escape.
- High-risk claim compliance: 100% of applicable critical controls with evidence and required human fact lock before scene production; a breach cannot be averaged away.
- Motion schema validity and duration/frame mismatch rate.
- Exact model/version adapters counted separately at DOCS_VERIFIED and RUNTIME_TESTED.
- Cinematic defect escape from actual handoff/render inspection.
- Adoption/usability: active projects, task completion, reviewer effort and opt-in friction feedback; minimize personal data.
- Governance completeness: applicable controls with evidence/status and unresolved P0/P1 count; NOT_RUN stays visible.

## J. Rekomendasi final

Pilih **EVOLUSI ADITIF + REFACTOR DOKUMENTASI TERBATAS**. No evidence requires redesign of M00/S01–S14, MCG or fail-closed governance. Gaps are motion data contract, model adapter evidence lifecycle, cinematic QA oracle and measured risk-proportional routing.

### Ten tindakan prioritas
1. Tetapkan S07 motion schema dengan half-open frames, keyframes, phases, units, easing dan source precision.
2. Tambahkan semantic validator dan positive/negative/edge tests.
3. Tambahkan S08 adapter schema dengan exact model/version, official docs, feature evidence, runtime refs dan recheck triggers.
4. Terapkan adaptive 9-slot video anatomy sebagai completeness check, bukan prompt universal kaku.
5. Integrasikan observable cinematic QA ke S12 dan gate yang ada.
6. Tegaskan S06 camera, S07 motion, S08 prompt, S10 renderer, S12 QA ownership.
7. Tambah beat/timecode handoff yang menghubungkan shot, motion, audio, overlay dan claims.
8. Definisikan R0–R3 routing dan pilot setelah baseline; unknown risk tidak pernah low.
9. Ukur cycle time, prompt iterations, defect escape, adapter verification, adoption/usability dan governance completeness.
10. Pertahankan S14 source parity/change audit; jangan klaim parity, CI, runtime atau release tanpa exact evidence/read-back.

## Scoring dan interpretasi

Nilai berikut adalah analytical rubric judgments untuk baseline source yang diperiksa, bukan pengukuran empiris.

| Dimensi | Bobot | Skor | Alasan |
|---|---:|---:|---|
| A. Integritas inti/governance | 25% | 4.4 | Claim/evidence, fail-closed, MCG, human approval, S14/S12 kuat; parity/review/runtime masih terbuka |
| B. Motion/cinematography | 15% | 2.9 | Frame/path/easing concepts ada; normalized motion record belum ada |
| C. Prompt anatomy/QA | 15% | 3.1 | Constraints ada; video 9-slot/cinematic oracle belum distandardisasi |
| D. Model portability | 10% | 3.1 | S08 conditional adapter ada; model/version registry/evidence lifecycle belum ada |
| E. Machine-readable output | 10% | 3.2 | Scene/claim/MCG schemas dan handoff ada; motion/adapter schema belum ada |
| F. Adoption/fast-track | 10% | 2.8 | Heuristic 1,000-candidate triage; no project lane/cycle-time evidence |
| G. Documentation/usability | 10% | 4.0 | Docs rinci; cognitive load dan friction belum diukur |
| H. Metrics/evaluation | 5% | 2.3 | Reports/status ada; adoption/usability/iteration outcomes belum terlihat |

Weighted total = 3.425, rounded to **3.43/5**. Sesuai rubrik, ini berada di kategori 2.5–3.4: cukup dengan intervensi struktural terbatas, dekat batas atas menuju kategori kuat. Skor baseline tidak boleh dipasarkan sebagai hasil empiris pasca-V4.1.7.

## Release and parity boundary

Source inspection does not prove runtime, renderer, actual media or human approval. Private Plugin Creator and GitHub remain distinct artifacts; matching version strings do not prove engine/source parity. Comparator was read-only. GitHub branch/PR is not a merge, license grant or production release. Production/public release remains HOLD while mandatory technical, rights, clinical, privacy, accessibility and human gates are open.
