
# Learning assets, external drift and project outcome contract — V4.1.9

**Status:** design contract. Tidak mengaktifkan scheduled monitoring, menyetujui formula, mengotorisasi risk pilot, atau membuat persistent telemetry.  
**Arsitektur:** M00 + S01–S14 tetap; no S15/S16 and no new production gate.

## 1. Approved Formula Ledger (AFL)

S01 owns intake/provenance; S08 owns prompt compilation/adaptation; S12 independently checks outputs; S13 owns continuity dependencies when MCG/Guides are involved; S14 records change/release trace; M00 orchestrates. S02 remains sole owner of health-claim interpretation and Fact Lock.

Each record requires:
- Stable formula_id, title, version, record_state, intended task/use.
- Source locator, source/retrieval date, contributor/owner, content hash and evidence grade.
- License/rights/attribution state and restrictions. Unknown rights means NOT_APPROVED.
- Scope: input type, audience/context, language, target output, exclusions and failure conditions.
- Exact prompt/formula or immutable reference; never silently alter accepted versions.
- Exact provider/model/version and task type when model-specific; otherwise PROVIDER_NEUTRAL.
- Feature evidence references and per-feature status; docs evidence is not runtime evidence.
- Test cases, expected/observed result, environment, output artifact ref, S12 QA and limitations.
- Claim refs only as references to current S02 records; earlier Fact Lock is not authority for a new project.
- Approval owner/date, expiry/recheck triggers, dependencies and rollback/supersession links.

Lifecycle: CANDIDATE → UNDER_REVIEW → APPROVED → STALE / REVOKED / REJECTED. Only APPROVED is discoverable as reusable. Stale/revoked/rejected/unknown never appear as current approved recipes. Model/version, provider feature, rights, MCG lock, material prompt edit or failure discovery triggers re-review. Reuse preserves provenance but inherits no clinical approval.

Community/Lanshu prompts are external untrusted inputs. Capture source, exact location, date, author where known, rights/attribution and evidence level. Do not scrape/copy corpus wholesale. Do not approve on popularity or one successful render. Pilot with non-clinical formulas. Require source+rights, scope, exact version evidence, reproducible oracle, S12 review and named human owner.

## 2. Model Drift Sentinel (MDS)

MDS detects possible changes in official provider documentation/endpoints and creates a review candidate. It never updates model capability or accepted baseline automatically.

**Observed snapshot:** immutable fetch attempt with endpoint, fetch time, HTTP result, normalized digest, full SHA-256, limited diff/extract, script version and errors.  
**Accepted baseline:** reviewer-confirmed digest and feature notes in a separate approved change/commit.

A changed observed snapshot must not overwrite accepted baseline. Fetch/parse failure, rate limit or endpoint removal creates an error event, not "no change", and never updates accepted digest.

Review lifecycle: DETECTED → TRIAGED → DOCS_VERIFIED / NOISE / SOURCE_UNAVAILABLE / REJECTED / BLOCKED. Runtime verification is a separate record requiring exact model version, environment, authorized run, inputs, outputs and observed oracle. Documentation change alone is not feature support.

Safety:
- Official allowlisted endpoints only; no arbitrary crawling or credential collection.
- No private/patient content in snapshots/logs.
- Review terms, robots, retention, redirects and access restrictions before activation.
- Full SHA-256; normalization rules versioned; minimize retained page content.
- Issue creation/retry must be idempotent. Failed issue creation must leave candidate detectable; no baseline advancement.
- Only named human reviewer can accept baseline. Rebaseline is explicit/logged and distinct from polling.
- Hash change never implies model approval, availability, clinical safety or release readiness.

Scheduler remains PROPOSED until endpoint allowlist, reviewer owner, permissions, baseline records, retry/notification, privacy/source review and rollback receive written approval. Start in shadow phase. Monitoring feeds S08 but does not amend adapter automatically.

## 3. Risk-Proportional Preflight Depth

S14 remains mandatory for every audit, change, source reconciliation, publication or release decision. Proportional means varying additional depth and avoiding duplicate capture—not skipping S14 or relaxing gates.

| Lane | Additional depth | Immutable controls |
|---|---|---|
| R0 LOW | Compact context/evidence summary only after explicit S02 NO_MATERIAL_HEALTH_CLAIM | Source scan, S02 disposition, rights/privacy/consent, continuity, S12 QA and human authority as applicable |
| R1 STANDARD | Normal source/context, dependency and release review | S02 claim review/Fact Lock, S12 QA and applicable rights/continuity/accessibility/human approval |
| R2 ELEVATED | Full context, claim/evidence dossier, specialist/human review, dependency closure and proof artifact QA | No fast-track; full evidence/review |
| R3 CRITICAL | Stop affected work, preserve evidence, notify owner, contain/retract if applicable | M00 cannot self-clear; authorized human resumption only |

Highest credible lane wins; critical trigger forces R3; UNKNOWN material risk is at least R2; critical triggers cannot be averaged against low dimensions. Downgrade requires evidence, named authority and reason. Fast-track remains inactive until separately authorized, measured, reversible pilot.

## 4. Model Selection Advisor (MSA) — bounded S08 function

Use only project constraints supplied or explicitly approved (purpose, modality, duration, audio, language, continuity, privacy, budget/region if provided, renderer/handoff).

Return at most three candidates, fit rationale, trade-offs, unsupported controls, unknowns, evidence refs and exact provider/model/version. Per-feature states:
- UNKNOWN / NOT_CHECKED
- DOCS_VERIFIED (official docs for exact version/feature)
- RUNTIME_TESTED (specific authorized run and evidence)
- STALE / BLOCKED / NOT_APPLICABLE

Advisor never declares a global best/approved/safe model, auto-selects, changes risk lane, bypasses S02 or transforms health claims. User/project remains selector. Prompt dialect is generated only for verified feature support. A model name in a matrix is not evidence.

## 5. Project Outcome Register (POR)

A privacy-minimized process record per project/release. Required fields: pseudonymous project/event ID, version, risk lane, input/output type, cohort/time window, metric definition, numerator, denominator, unit, value, missingness, evidence locator, owner, confidence/limitation and review date.

Allowed process metrics: cycle time to S12 handoff; active reviewer effort; rework/reopen; first-pass package acceptance; approved formula reuse; stale evidence found/detection latency; trace completeness; risk misclassification; major/critical QA escapes; mapping defects.

No new patient/audience behavioral-health data, clinical effect claims, inferred health outcomes or unsupplied analytics. Social engagement/algorithm metrics only when explicitly supplied and authorized for a specific project. No audience surveillance or persistent personal telemetry is implied.

Always report numerator, denominator, cohort, window, missingness and caveat. Stratify by risk lane, complexity and input mode. No composite score or target before representative baseline. NOT_MEASURED stays visible.

## 6. Ownership and change invalidation

| Function | Owner |
|---|---|
| Source/rights intake | S01 |
| Clinical meaning, evidence, Fact Lock | S02 only |
| Formula prompt compilation/adaptation and model advisor | S08 |
| Independent reuse/formula QA | S12 |
| MCG/Guide continuity dependencies | S13 |
| Context, external drift and release parity | S14 |
| Workflow/status/outcome aggregation | M00 |

Changes to source, model/version, feature docs, prompt text, rights, claims, MCG locks, scene/motion or renderer invalidate dependent records. QA/approval refs must rebind to new hashes and rerun. Stale evidence never becomes PASS by inference.

## 7. Minimum acceptance for future implementation

- No new specialist or production gate.
- Full provenance for reusable formulas and drift events.
- No auto-approval, auto-rebaseline or auto model selection.
- No status promotion from NOT_RUN / NOT_VERIFIED / BLOCKED / HOLD / STALE without matching evidence and authorized owner.
- S02 sole clinical interpretation and S14 mandatory preflight unchanged.
- R0–R3, highest-lane-wins, UNKNOWN >= R2 and critical override unchanged.
- Trace source/claim → beat → scene/shot → motion → renderer layer → QA oracle remains intact.
- No clinical outcome claim, new audience behavior collection or unsupplied analytics.
- Any pilot has baseline, denominator, independent adjudication, pass/fail, rollback owner and stop triggers before activation.
