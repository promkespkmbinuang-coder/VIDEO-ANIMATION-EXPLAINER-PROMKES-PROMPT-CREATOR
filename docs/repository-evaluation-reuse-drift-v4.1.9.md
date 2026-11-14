# PROMKES × Lanshu — repository audit and V4.1.9 development plan

Audit date: 2026-11-14. Target: PROMKES public GitHub repository. Comparator only: cclank/lanshu-awesome-ai-video-kit. Companion baseline: private Plugin Creator V4.1.9 read back separately. Conclusions are limited to retrieved source files, PR/commit metadata and CI records.

## 1. Executive findings

1. PROMKES is a health-first evidence-gated production compiler; Lanshu is an extensible prompt/formula knowledge kit. Feature parity is not the goal.
2. Public target main is V4.1.8 at 8b3fe9f09ac0f193e49ae7df36937668e69c065d. PR #24 V4.1.9 was reverted by PR #25; revert rationale is UNKNOWN.
3. Private Plugin Creator is V4.1.9 and already has a Learning–Asset–Drift–Outcome design contract, but reviewed files had no dedicated executable registry schema/validator/tests for the five functions.
4. PR #24 CI was misreported in its old context register: exact-head run 43407423582 succeeded and recorded 120 passed; link run 43407423425 succeeded (17 links, 0 errors). This does not explain PR #25 or prove runtime readiness.
5. The leverage point is sedimenting project successes into discoverable, rights-cleared, scope-bound, hash-addressed reusable patterns with independent QA and dependency invalidation—not weakening evidence gates.
6. Lanshu's monitor saves new hashes during the observation run before issue delivery is confirmed. A failed alert can leave a new baseline and hide unresolved change on the next run. Raw copying is unsafe.
7. This patch retains 15 skills, adds no S15/S16 and no new production gate. Scheduler, baseline acceptance, R0/R1 fast-track, model auto-selection and release approval remain inactive/human-controlled.

## 2. Genetic map: system species

| Dimension | PROMKES | Lanshu | Decision |
|---|---|---|---|
| Primary object | Approved health-promotion production artifacts | AI-video prompt knowledge | Keep distinct identity |
| Truth authority | S02, evidence gate and human approval | Source-labelled prompt/method assets | Never import authority assumptions |
| Change governance | M00 + mandatory S14 | Contribution and monitoring workflow | Adopt review queue, not auto-accept |
| Assets | Source/claim/beat/scene/motion/render/QA trace | Prompt library and cross-model matrix | Add typed, scoped formula ledger |
| Model choice | Versioned adapters; S08 | Static model selector | Evidence-labelled advisory shortlist |
| Drift | Adapter evidence; no auto-accept | Weekly endpoint hash checks | Immutable observation + accepted baseline split |
| Community learning | Controlled source and rights intake | Issue templates and contribution guide | Adapt contribution trust tiers |
| Outcomes | Process KPI blueprint | Library counts and ratings | Process-only records, no clinical/audience telemetry |

## 3. Gap matrix

| Lanshu pattern | Target gap/risk | Decision |
|---|---|---|
| Prompt/formula library | No approved reuse registry in public V4.1.8 | ADAPT with provenance, rights, scope, version, hash, S12 and human approval |
| Model-selector shortlist | Static version claims can stale | ADAPT to S08, max 3 candidates, exact-version evidence, no auto-select |
| Cross-model examples | Matrix not proven end-to-end performance | ADAPT as tested patterns; separate template and runtime tests |
| Endpoint hash monitor | Auto-advancing baseline and alert failure coupling | ADAPT MDS with immutable observation and separate accepted baseline |
| Community contribution UX | Self-rating may bias evidence | ADAPT into S01 intake, classify evidence tier |
| Offline local UI | Additional maintenance without proven bottleneck reduction | DEFER |
| Lanshu MIT license | Covers Lanshu repository content only | REJECT inference that it permits copying into PROMKES |

## 4. Operational status audit

| Capability | Status before patch | Missing proof / impact |
|---|---|---|
| Public package | VERIFIED V4.1.8 | V4.1.9 patch branch/PR pending |
| Private package | VERIFIED metadata/read-back V4.1.9 | Byte parity NOT_VERIFIED |
| S02 and S14 ownership | PRESENT IN POLICY | Full historical coverage remains PARTIAL |
| R0–R3 routing | STATIC VALIDATOR PRESENT | Pilot/baseline NOT_MEASURED; no fast-track |
| Source-to-QA trace | SCHEMAS/CONTRACTS PRESENT | Actual renderer/MP4 QA not run |
| AFL | NOT_PRESENT operationally in public V4.1.8 | Persistent registry/retrieval still unimplemented |
| MDS scheduler | NOT_ACTIVATED | Endpoint, permission, owner, live tests, reliability |
| MSA | INSTRUCTION-LEVEL | Actual model feature evidence remains unknown |
| POR | KPI blueprint only | Outcome baseline cohort not measured |
| GitHub scenario suite | NOT_RUN, 45 cases | New unit tests do not close it |
| Private acceptance suite | NOT_RUN, 20 cases | Separate namespace; no conflation |
| Host/runtime/AI/ASR | NOT_RUN/NOT_VERIFIED | No capability claim |
| Renderer/MP4 | NOT_RUN | Mapping does not prove render |
| Human/clinical/legal/rights release | HOLD | No artifact-bound authorization |

## 5. Root-cause analysis

### RC-1 — successful work not productized as reusable assets (HIGH)
Approved outputs are project-specific and knowledge remains embedded in prose/conversation. No tested path promotes a pattern into a rights-cleared, versioned, scoped asset. Add AFL; do not loosen Fact Lock.

### RC-2 — observation and accepted baseline coupled (HIGH)
Documentation change, model feature change and runtime proof are distinct. A failed fetch or undelivered issue cannot mean stability. Lanshu's baseline update timing is the key failure mode to avoid.

### RC-3 — governance text exceeds executable enforcement (HIGH)
Private V4.1.9 defines good rules, but without record schemas and semantic tests they remain instruction-level. This patch enforces record invariants only; it does not create services or storage.

### RC-4 — preflight cost is not decomposed or measured (MEDIUM)
Required decisions and duplicate clerical capture are conflated. No measured evidence shows the gate itself is the bottleneck. Pilot only administrative depth; keep S14 and risk isolation fixed.

### RC-5 — outcomes lack denominator/evidence discipline (MEDIUM)
KPI vocabulary exists without a validated cohort pipeline. Require numerator, denominator, time window, missingness and source evidence; no clinical or audience telemetry.

## 6. Five recommendations in decision format

### AFL-01 — Approved Formula Ledger
Severity HIGH; type Preventive; effort M; impact L. Root cause: unsedimented project knowledge. Owner path: S01 rights/provenance → S08 scoped retrieval → S12 independent QA → human approval → M00 gate. Guardrail PASS by design: formula never carries Fact Lock, S02 remains sole clinical interpreter. Pilot: one non-clinical visual/motion formula; compare two projects in identical scope against no-reuse control. Accept only if rights CLEAR, provenance, exact scope/model, test evidence, S12 PASS and human approval bind exact SHA. Roll back by STALE/REVOKED, suppress retrieval, preserve snapshots and invalidate dependents. Residual: small-sample bias and rights interpretation. P0 record contract; P1 pilot.

### MDS-01 — Model Drift Sentinel
Severity HIGH; type Evaluative; effort M; impact L. Root cause: model/docs drift has no governed review path. Owner S14 observation, S08 feature impact. Guardrail PASS: observation never promotes capability. Pilot manual capture of three official endpoints over four weeks; no scheduler. Accept: fetch failure SOURCE_UNAVAILABLE, normalizer change review, hash change review, accepted baseline moves only with human evidence. Rollback disable fetch and retain old baseline and unresolved observations. Residual: between-poll changes, dynamic docs and semantic drift. P0 immutable records; P2 scheduler.

### RPF-01 — Risk-Proportional Preflight
Severity HIGH; type Preventive; effort M; impact M. Root cause: duplicate admin capture not separated from core controls. Guardrail PASS only with S14 COMPLETE in every lane; UNKNOWN at least R2; highest trigger wins; critical forces R3; R2/R3 no fast-track; fast-track false. Pilot shadow-only; current workflow unchanged. Accept zero missed critical trigger, zero under-routing, 100% S14 completion; any miss stops pilot. Roll back to existing full preflight. Residual context misclassification. P0 no-bypass enforcement; P1 shadow pilot.

### MSA-01 — Model Selection Advisor
Severity MEDIUM; type Evaluative; effort S; impact M. Root cause: model comparison is scattered and static. Owner S08. Guardrail PASS: up to three candidates, exact model version, feature evidence or UNKNOWN; no global-best claim, automatic selection, capability promotion or risk change. Pilot one no-render prompt task. Accept complete feature status and explicit USER/PROJECT_OWNER choice. Roll back to provider-neutral prompts. Residual documentation/runtime divergence. P1.

### POR-01 — Project Outcome Register
Severity MEDIUM; type Evaluative; effort S-M; impact M. Root cause: KPI names without cohort/denominator. Guardrail PASS: process-only whitelist, no new patient/audience behavior data or clinical effects. Pilot retrospective sample from existing process records only. Accept every metric with numerator, denominator, cohort, time window, missingness, evidence and limitations. Roll back by stopping collection and retaining only authorized process records. Residual small-sample/case-mix bias. P1.

## 7. Additional findings

- Lanshu README totals are internally inconsistent (e.g. 594/604 and 22/24); counts are not quality evidence.
- Its prompt translator explicitly says the 110-item matrix is not based on end-to-end tested video performance.
- Endpoint list includes broad/unofficial homepages; wan-2.5 identifier references version 2.7. Hashing a page does not prove a model feature.
- PR #24 CI failure claim is contradicted by exact Actions logs; PR #25 rationale is unknown.
- Public 45-case and private 20-case suites remain distinct; pytest count does not close either.
- The first AFL schema validates `rights_status=CLEAR` as a declared state, but does not yet require a rights-holder reference/evidence locator or cryptographically verify the approver. Do not treat this as verified rights clearance; add evidence references and authorized-review binding before an actual APPROVED ledger is populated.
- MSA record shape permits a feature status such as `DOCS_VERIFIED` with a null evidence reference; add a semantic rule that verified statuses require evidence. POR checks denominator presence but does not independently recompute each `value` from metric-specific numerator/denominator semantics. These require follow-up hardening before production reporting.
- RPF enforces consequences of declared `material_unknown` and `critical_trigger` flags; it does not itself discover every critical trigger from source context. Correct trigger detection remains M00/S14 responsibility and must be independently checked in shadow pilot. MDS is a pure comparison helper; it does not fetch/allowlist endpoints, persist observations or run a scheduler.

## 8. Roadmap

P0: schema, semantic validator, tests, manifests and skill-owner additions; resolve branch CI and independent review. P1: manual AFL pilot; RPF shadow-only pilot; MSA advisory pilot; retrospective POR baseline. P2: MDS scheduler only after official endpoint/terms/security/owner/retry/retention/rollback criteria; optional local search UI only if measured benefit warrants maintenance.

## 9. File-level patch map

- schemas/v4/learning-governance.schema.json — AFL/MDS/baseline/MSA/POR/RPF record contracts.
- scripts/learning_asset_engine.py — strict JSON, semantic validation, pure drift compare and preflight plan.
- tests/test_learning_asset_governance.py — rights/hash/S12, reuse, drift errors, model advice, risk and outcome regressions.
- .github/workflows/validate.yml — schema-check in static CI.
- M00, S01, S08, S12, S13, S14 SKILL.md — ownership-specific workflow only.
- both manifests, README, CHANGELOG, metrics and V4.1.9 context register — release/context trace.

## 10. Success metrics

Measure cycle time; reviewer effort; rework loops; approved reuse ratio; stale evidence detection latency; trace completeness; risk-lane disagreement under shadow review; escaped critical QA defects; S14 completion; AFL rights rejection. Every measure needs numerator/denominator, cohort, period and evidence. Baseline and target remain NOT_MEASURED until an actual cohort exists.

## 11. Residual risks and mitigations

Official documentation may lag runtime; keep docs/runtime status separate. Rights may be misread; require a named rights owner. Formula reuse may alter factual meaning; re-run S02 on each claim and S12 on output. Hash equality is not truth; human diff remains. Polling misses between-interval changes; report cadence. Metrics may bias work; minimize process fields and retention. Risk triage may miss context; mandatory S14 and R2 fallback. Private/public code may diverge; per-file read-back and hashes, not equal versions.

## 12. Assumptions and evidence unavailable

Private read-back proves metadata and inspected text, not byte/runtime parity. No live endpoint fetch/scheduler was run. Lanshu counts/features are self-reported. PR #25 rationale UNKNOWN. PR #24 CI is exact-head static evidence only. PR #26 exact head `ec0d1b59ad8c2d0d4922baa7a40ec26af6517a4e` passed schema-check, strict package validation, manifest consistency, all 134 pytest checks and link validation (workflow runs `43561043130` and `43561043129`). The initial head `a32d90197...` had 5 failing tests because isolated sub-schema references could not resolve; the validator was corrected and the rerun passed. PR #26 remains draft/open with no independent review, no merge and no post-merge main CI. Live host invocation, external AI/ASR/TTS, scheduler, renderer bundle/render, MP4 inspection, accessibility user test and clinical/legal/rights approvals remain NOT_RUN/NOT_VERIFIED/HOLD.

**Release boundary:** The five features are record-contract and static-validation additions only. They do not authorize production release, scheduler activation, automatic approvals, health interpretation or lane relaxation.
