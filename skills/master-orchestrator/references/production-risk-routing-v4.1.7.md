# M00 Addendum — Risk-Proportional Routing (V4.1.7)

This policy operates within existing M00/S02/S12/S14 ownership. It creates no S15, no new gate and no waiver path.

## Risk lanes

- **R0 — LOW / NON-CLAIM:** no material health claim, clinical instruction, statistic, diagnosis/treatment/prevention promise, sensitive personal data, unresolved rights or contested source. A no-claim finding is explicit and traceable.
- **R1 — STANDARD:** routine health promotion with sourced claims within approved guidance; no elevated-risk instruction or unresolved conflict.
- **R2 — ELEVATED:** clinical advice, dosage/treatment, vulnerable groups, high-impact statistics, outbreak/emergency or disputed evidence. Full evidence, specialist and human review.
- **R3 — CRITICAL:** potential serious harm, contradicted/fabricated claim, privacy/consent breach, rights/authority failure or unauthorized publication. Stop and escalate.

Unknown or ambiguous risk is never R0; use the more protective route pending resolution.

## Allowed efficiencies

Consolidate duplicate metadata capture; reuse approved templates and Guide refs; parallelize independent source/audio/rights checks; automate deterministic schema tests; use dependency-based regression where safe; and record justified NOT_APPLICABLE dispositions.

## Mandatory controls

Do not skip source classification, untrusted-input handling, S02 authority for any material health claim, claim-to-scene traceability, rights/privacy/consent, applicable MCG continuity, independent S12 QA, accessibility or authorized human release approval. No route may promote NOT_RUN, UNKNOWN, NOT_VERIFIED or BLOCKED to PASS. No predecessor gate may be bypassed.

## Pilot requirement

R0/R1 routing remains a proposal until a reversible, measured pilot establishes cycle-time and reviewer-effort baselines while monitoring claim misses, rights/privacy defects, rework, QA escape and misclassification. Stop the pilot on any serious gate escape and revert to standard routing.
