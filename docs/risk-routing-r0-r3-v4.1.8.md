# Risk routing R0–R3 — V4.1.8

**Status: IMPLEMENTED AS A PROPOSED CONTROL CONTRACT; OPERATIONAL PILOT NOT AUTHORIZED.** This is a conservative routing rubric, not a validated clinical risk instrument and not a substitute for institutional risk policy.

## Decision rule

Assess the highest credible harm across health/clinical, vulnerable audience, evidence uncertainty, privacy/consent, rights, public reach/reversibility, and production integrity. The highest triggered lane wins. Do not average dimensions: one critical trigger is sufficient for R3. Missing or ambiguous material information routes at least R2 until resolved; it is never silently R0.

### Lanes

| Lane | Meaning | Examples (illustrative, not exhaustive) | Required route |
|---|---|---|---|
| R0 | Low / non-claim | Purely administrative/celebratory visual with no health instruction, no material health claim/statistic, no personal data, clear rights and reversible scope | Compact workflow; explicit S02 no-material-claim disposition; normal rights/privacy/brand/accessibility checks; S12 package QA |
| R1 | Standard | Routine health-promotion message using approved, current, sourced guidance; low ambiguity; no high-risk instruction or sensitive-data exposure | Standard S01–S14 route with targeted evidence checks; S02 claim review/Fact Lock; MCG as applicable; independent S12 |
| R2 | Elevated | Advice that could materially affect care-seeking or behavior; dosage/treatment; pregnancy/children/other vulnerable groups; high-impact statistics; outbreak/emergency; disputed, incomplete or context-sensitive evidence; high-reach or difficult-to-retract content | Full S02 evidence dossier and specialist review; human clinical/institutional review; rights/privacy/consent review; proof artifact and independent S12 review; explicit release authority |
| R3 | Critical / stop-and-escalate | Plausible serious harm; fabricated/contradicted dangerous instruction; identifiable patient data without valid authority; absent consent/rights where exposure is material; impersonation, unauthorized publication, compromised source or deliberate gate evasion | Stop affected output and distribution; preserve evidence; notify authorized human owner; contain/retract if already released; correct, invalidate dependents, retest and obtain explicit authorized clearance |

## Non-negotiable overrides

1. Any plausible serious-harm instruction or known materially false claim => R3.
2. Sensitive personal/health data without documented lawful basis, minimization and consent/authority where required => R3.
3. Rights/consent/authority unresolved for an asset that will be published => at least R2; suspected infringement or unauthorized disclosure with material exposure => R3.
4. Dosage, treatment, diagnosis, emergency triage, vulnerable populations, outbreak guidance or contested evidence => at least R2.
5. Unknown source, unknown audience, unknown intended use, missing approval or untested model/renderer does not lower risk. Classify the affected dimension UNKNOWN and hold dependent work.
6. Any R3 trigger cannot be offset by a low score elsewhere. Risk downgrade requires written evidence, named accountable reviewer and reason.

## Triage record

Every project records: `risk_assessment_id`, project/version, assessor/date, intended audience/use/channel/reach, each dimension status (`LOW|STANDARD|ELEVATED|CRITICAL|UNKNOWN`), trigger evidence, highest lane, rationale, required reviewers, residual risks, expiry/reassessment trigger, decision owner and approval state.

Reassess when claims, audience, assets, data, platform/reach, model, renderer, scene/overlay, rights, or release scope changes. Reassess after a defect, complaint, new evidence or policy change.

## Lane-specific workflow

- R0 may use compact documentation only after S02 explicitly records `NO_MATERIAL_HEALTH_CLAIM`; this is not a clinical waiver. S12, rights, privacy, accessibility and human release controls still apply.
- R1 follows normal gates. Efficiency means removing duplicate capture, not removing owner checks.
- R2 requires evidence and human review before final copy/visual lock and before publication. Proof render and independent artifact QA are required when a rendered asset is intended.
- R3 suspends affected workflow. M00 cannot self-clear; only the authorized accountable human owner can authorize resumption after documented remediation.

## Fast-track pilot guardrails

R0/R1 pilot may begin only after written sponsor approval, named pilot owner, S02/S12 concurrence, approved sample definition, privacy-minimized logging, baseline collection and rollback readiness. R2/R3 are excluded. Start in shadow mode (recommendations logged, existing standard route unchanged), then limited controlled pilot after review. Stop immediately for a serious claim miss, privacy/rights incident, unauthorized release, critical continuity defect, or evidence gate escape. Also pause for a material rise in major QA escapes or unexplained misclassification. No numeric target is set before baseline.

## Status vocabulary

`PROPOSED`, `SHADOW_MODE`, `PILOT_APPROVED`, `PILOT_ACTIVE`, `PAUSED`, `ROLLED_BACK`, `EVALUATED`. Current repository status is `PROPOSED`; R0/R1 fast-track is not active. A lane assignment is not approval to publish.
