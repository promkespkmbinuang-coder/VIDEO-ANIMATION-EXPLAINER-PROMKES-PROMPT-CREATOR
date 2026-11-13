# V4.1.7 — Risk-Proportional / Fast-Track Governance Proposal

**Status:** proposed routing policy for validation. It is not a gate bypass and does not prove production time has fallen. It operates within existing M00/S02/S12/S14 ownership and gate architecture.

## 1. Principle

Fast-track means less duplicate paperwork and more efficient sequencing for demonstrably low-risk work. It does not mean automatic clinical NOT_APPLICABLE, no human approval, or release without evidence. Unknown risk is never low risk.

## 2. Risk lanes

| Lane | Entry conditions | Routing | Release constraints |
|---|---|---|---|
| R0 — LOW / NON-CLAIM | No material health claim, clinical instruction, statistic, diagnosis/treatment/prevention promise, sensitive personal data, unresolved rights or contested source; scope limited and reversible | Compact intake, one source/asset dossier, template-driven creative work, consolidated static QA | Rights/privacy/consent and brand checks remain; S02 no-claim disposition is explicit and traceable; S12 static QA and authorized release decision remain |
| R1 — STANDARD | Routine health promotion with sourced claims within approved guidance; no elevated-risk instruction or unresolved conflict | Normal S01–S14 path with targeted rather than duplicated checks | S02 claim review/fact lock, source trace, continuity, S12 and applicable human approvals remain |
| R2 — ELEVATED | Clinical advice, treatment, dosage, vulnerable groups, high-impact statistics, outbreak/emergency or disputed/ambiguous evidence | Full evidence review, specialist escalation, detailed clinical/rights/privacy review, proof render and independent artifact QA | Fail-closed on unresolved material claims, unsupported wording or missing authorization |
| R3 — CRITICAL / STOP-AND-ESCALATE | Potential serious harm, unsafe medical instruction, fabricated/contradicted claim, privacy/consent breach, unauthorized release or serious rights issue | Stop affected deliverable, preserve evidence, escalate to authorized humans, remediate and retest | No fast-track; explicit authorized resolution required before resumption |

A user-facing lane is an operational routing aid, not a clinical risk score. Record rationale, source evidence, reviewer and re-triage trigger. When assignment is ambiguous, use the more protective lane.

## 3. Safe efficiencies

- combine repeated metadata capture into one versioned intake record;
- reuse approved templates, Guide references and schemas without copying locked content;
- parallelize only independent source/audio/rights checks;
- automate deterministic schema/static tests;
- run targeted regression based on dependency closure while retaining mandatory high-risk regression;
- use concise review records for clear low-risk cases;
- allow NOT_APPLICABLE only with named criterion, evidence of non-applicability, rationale and reviewer/owner.

## 4. Non-skippable controls

Source classification and untrusted-input handling; health claim scan and S02 ownership; source/claim/message/scene/overlay traceability; rights/privacy/consent/brand authority; MCG continuity where applicable; independent S12 QA; accessibility; and human clinical/legal/institutional/release approval where required.

No lane may promote NOT_RUN, UNKNOWN, NOT_VERIFIED or an unreviewed assumption to PASS. No lane overrides a predecessor gate.

## 5. Pilot and rollback

Before operational adoption, run a reversible pilot on a representative low-risk sample. Capture intake-to-handoff timestamps, reviewer effort, iteration count, static QA defects, reopened gates, misclassification and downstream rework. Compare cohorts only when scope, platform, input type and review needs are sufficiently comparable. Establish a baseline before targets.

Rollback to standard routing if claim misses, rights/privacy defects, critical continuity issues, QA escape or misclassification increase. Stop the pilot on a serious gate escape.
