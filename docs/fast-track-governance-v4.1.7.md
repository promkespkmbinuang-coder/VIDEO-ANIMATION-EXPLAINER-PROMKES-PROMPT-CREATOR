# V4.1.8 — Risk-Proportional Routing R0–R3 and controlled-pilot governance

**Status:** Operational contract implemented for review; R0/R1 fast-track remains PROPOSED and inactive. This is not a validated clinical risk instrument, policy waiver or gate bypass.

## 1. Decision rule

Assess health/clinical harm, audience vulnerability, evidence uncertainty, privacy/consent, rights/authority, public reach/reversibility and production integrity. The highest credible risk determines the lane. Never average away a critical trigger. Unknown or ambiguous material risk is at least R2 until resolved; it is never R0.

## 2. Four lanes

| Lane | Definition | Routing |
|---|---|---|
| R0 — LOW | Non-claim, low-impact, reversible work; no material health claim/instruction/statistic, sensitive data, unresolved rights or source conflict | Compact intake only after explicit S02 NO_MATERIAL_HEALTH_CLAIM; rights/privacy/brand/accessibility and S12 remain |
| R1 — STANDARD | Routine health promotion using current, sourced, approved guidance; no elevated-risk instruction or unresolved conflict | Standard S01–S14 route, S02 claim review/Fact Lock, MCG as applicable and independent S12 |
| R2 — ELEVATED | Treatment/dosage/diagnosis advice, vulnerable groups, high-impact statistics, outbreak/emergency, disputed evidence or material uncertainty | Full evidence dossier, specialist + human clinical/institutional review, rights/privacy review, proof artifact and independent S12 |
| R3 — CRITICAL | Plausible serious harm, materially false dangerous instruction, unauthorized sensitive data/asset disclosure, unauthorized publication or deliberate gate evasion | Stop and contain; preserve evidence; escalate to authorized human; remediate, invalidate dependents, retest and obtain explicit clearance |

A single R3 trigger sets R3. Dosage/treatment, children/pregnancy/other vulnerable populations, emergency/outbreak guidance and contested evidence are at least R2. Suspected serious privacy/rights/consent breach is R3. Missing approvals never lower risk.

## 3. Triage record and reclassification

Record assessment ID, project/version, assessor/date, intended audience/use/channel/reach, dimension ratings (LOW|STANDARD|ELEVATED|CRITICAL|UNKNOWN), evidence refs, triggers, highest lane, rationale, required reviewers, residual risk, expiry/reassessment triggers, decision owner and approval state. Reassess after claim/source/audience/asset/data/platform/model/renderer/scene/overlay/rights changes, new evidence, complaint or defect. Downgrade requires written evidence and named accountable reviewer.

Executable helper: scripts/validate_risk_assessment.py. It enforces conservative maximum-lane selection and R3 overrides; it is triage support only, not a clinical determination or publication authorization.

## 4. Non-skippable controls

Source classification/untrusted-input handling; S02 authority for all material health claims; claim-to-scene/overlay traceability; rights/privacy/consent/brand; MCG continuity where applicable; independent S12 QA; accessibility; and authorized human clinical/legal/institutional/release approval where required. No lane promotes NOT_RUN, UNKNOWN, NOT_VERIFIED, BLOCKED or assumptions to PASS.

## 5. Controlled R0/R1 pilot

R0/R1 remains inactive until written sponsor approval, named pilot owner, S02/S12 concurrence, privacy-minimized logging, defined cohort, baseline collection, independent shadow adjudication and rollback readiness. Start in shadow mode; only then consider limited controlled operation. R2/R3 excluded. Stop on serious claim, privacy, rights, authorization, continuity or QA gate escape. KPI definitions and baseline protocol: docs/pilot-kpi-baseline-v4.1.8.md.

## 6. Status

PROPOSED, SHADOW_MODE, PILOT_APPROVED, PILOT_ACTIVE, PAUSED, ROLLED_BACK, EVALUATED. Current state: PROPOSED. This contract does not imply sponsor approval, measured cycle-time improvement or live pilot operation.
