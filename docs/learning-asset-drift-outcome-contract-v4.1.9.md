# V4.1.9 — Learning, Asset, Drift and Outcome Governance Contract

**Status:** design and static validation contract. This document does not activate persistent storage, a monitoring scheduler, external provider runtime, automatic approvals or release.

## 1. Architecture and authority

No new subskill and no new production gate. M00 orchestrates; S01 owns source/rights intake; S02 exclusively owns health-claim interpretation and Fact Lock; S08 owns formula retrieval/adaptation and model selection advice; S12 owns independent QA; S13 owns continuity dependency refs; S14 owns cross-conversation/release preflight and model-drift observation/review. Humans retain rights, clinical, legal, institutional and release authority.

The validator scripts/learning_asset_engine.py checks supplied records against schemas/v4/learning-governance.schema.json. It is deterministic static validation, not a database, service, scheduler, fetch client, cryptographic identity check or authorization service.

## 2. Approved Formula Ledger (AFL)

Lifecycle: DRAFT → CANDIDATE → REVIEWED → APPROVED → STALE/REVOKED. Transitions are not automated. An APPROVED record requires source locator/snapshot, source type and observed date; CLEAR rights with explicit rights-holder/permission basis; task, audience, language, exclusions and known failure modes; exact provider/model/version or explicit provider-neutral binding; at least one PASS validation run with durable evidence; independent S12 PASS with reviewer and evidence; and authorized human approval bound to exact content SHA-256.

Retrieval fails closed: only APPROVED, rights-cleared, scope-matched records are eligible. Any mismatch, missing permission, changed hash, unsupported model version or stale evidence removes the item from reuse and triggers review. A formula is a production pattern, not a claim registry. It may reference claim IDs only; S02 re-evaluates every health claim in each project and retains exclusive Fact Lock authority.

## 3. Model Drift Sentinel (MDS)

Store every successful observation as an immutable snapshot: endpoint identity, exact URL, provider/model, observed time, fetch/HTTP/parse status, normalizer version, normalized hash, snapshot reference and change summary. Failed fetch, rate limit, blocked redirect, parse failure or policy denial is SOURCE_UNAVAILABLE, never NO_CHANGE.

Compare observation with a separate HUMAN_ACCEPTED baseline. Changed content, endpoint identity or normalizer version creates REVIEW_REQUIRED. A successful fetch alone cannot change the accepted baseline. A human reviewer must inspect source authority, diff, model/version, feature impact, terms and downstream artifacts before explicitly accepting a new baseline. Alert-delivery failure must not erase unresolved change.

A scheduler is NOT_ACTIVATED. Before activation require official endpoint allowlist, source/terms review, owner, permission, bounded timeouts/retries, rate limits, safe redirect policy, immutable snapshots, idempotent alerts, audit records, failure handling, retention limits, rollback and security review. Monitoring documentation does not prove a model feature or runtime capability.

## 4. Risk-Proportional Preflight (RPF)

All lanes retain mandatory S14 COMPLETE preflight and all required safety, rights, privacy, source, claim, continuity, QA and human approvals. RPF may reduce duplicate clerical capture or select additional review depth only:
- R0: COMPACT administrative depth; explicit S02 NO_MATERIAL_HEALTH_CLAIM required.
- R1: STANDARD depth.
- R2: FULL depth; no fast-track.
- R3: STOP_AND_ESCALATE; no fast-track.
- UNKNOWN material risk: at least R2.

Highest credible trigger wins; critical trigger forces R3; no averaging or override can downgrade it. Incomplete S14 blocks every lane. Fast-track remains false/inactive; this contract does not authorize a pilot.

## 5. Model Selection Advisor (MSA)

S08 may return no more than three candidates with exact provider/model/version and feature-level status: DOCS_VERIFIED, RUNTIME_TESTED, UNKNOWN, NOT_CHECKED, STALE or BLOCKED. Each supported feature includes evidence. Present task fit, trade-offs, limitations and explicit unknowns. Cost, latency or availability only appear when evidence exists. No global best/safest ranking, automatic selection, capability promotion or risk-lane change. USER/PROJECT_OWNER selects.

## 6. Project Outcome Register (POR)

Only privacy-minimized process metrics: cycle time, reviewer effort, rework rate, first-pass acceptance, approved formula reuse rate, stale evidence detection latency, trace completeness, risk misclassification and QA escape count. Each observation has cohort, window, numerator, denominator, unit, missing count, evidence and limitations. Zero denominator means undefined value. Report small samples and missingness; never claim causal improvement from descriptive association.

No new audience/patient behavioral-health data, clinical-effect claims, unsupplied analytics, personal identifiers or platform engagement metrics are collected. Do not invent baseline, targets or improvements before a measured cohort exists.

## 7. Traceability and invalidation

Maintain source → approved claim/Fact Lock → beat → scene/shot → motion → renderer layer → QA oracle and link AFL/MDS/advice/outcome records through stable IDs. Formula, source, model-version, MCG, scene or renderer changes trigger dependency closure: mark affected artifacts STALE/INVALIDATED, preserve previous snapshots, rebuild minimum dependents, rerun relevant tests and renew approvals bound to superseded hashes. No unchanged upstream approval is copied to changed artifacts.

## 8. Validation and evidence boundaries

Run python scripts/learning_asset_engine.py schema-check, validate a supplied governance bundle, and python -m pytest -q. These checks validate schema and semantics for supplied records. They do not test live endpoints, scheduler reliability, human identity/authority, rights, clinical truth, ChatGPT invocation, external AI, ASR/TTS, renderer integration, render/export, MP4/media quality or institutional approval. Existing GitHub 45-case scenario suite and private 20-case suite remain separately NOT_RUN until each case has its own oracle and execution evidence.

## 9. Failure and rollback

Fail closed on missing provenance, uncertain rights, hash mismatch, stale evidence, unverified model binding, incomplete S14, inconsistent risk, missing S12 review or approval mismatch. Rollback sets the record STALE/REVOKED, suppresses retrieval, preserves snapshots and the prior accepted baseline, invalidates dependent approvals and reruns S12 checks. No recovery may bypass S02 or S14.
