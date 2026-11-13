# R0/R1 pilot — baseline and KPI protocol (V4.1.8)

**Current status: NOT MEASURED / NOT APPROVED.** No numeric baseline, target, or achieved improvement is claimed.

## Evaluation questions
1. Can R0/R1 routing reduce avoidable handoff delay and reviewer effort without increasing clinical, rights, privacy, continuity or QA escapes?
2. Can users correctly complete intake, trace a beat to its source/motion/audio/overlay, and understand status/limitations?
3. Does Remotion mapping preserve the canonical motion contract for the exact pinned runtime tested?

## Baseline before pilot
Collect at least one representative observation period under current standard workflow. Define cohort and sample before collection; stratify by input mode, lane, complexity, channel, and whether rendering is required. Do not compare unlike cohorts. Use privacy-minimized event IDs; no patient-identifying content in telemetry.

| KPI | Operational definition | Baseline | Target | Owner / cadence |
|---|---|---|---|---|
| Adoption | Eligible R0/R1 cases using proposed workflow ÷ all eligible cases | NOT MEASURED | Set after baseline | Pilot owner / weekly |
| Task completion | Cases completing required artifacts without facilitator rescue ÷ started cases | NOT MEASURED | Set after baseline | Product owner / weekly |
| Usability | Standardized task success + post-task ease score; report response rate and sample | NOT MEASURED | Set after baseline | Independent evaluator / cohort |
| Cycle time | Median and P90 elapsed time from accepted intake to S12 handoff; separate external wait | NOT MEASURED | Set after baseline | Operations / weekly |
| Reviewer effort | Active review minutes per case, by lane and role | NOT MEASURED | Set after baseline | Review lead / weekly |
| Rework | Cases reopening upstream gates or requiring material correction ÷ completed cases | NOT MEASURED | No increase vs baseline | S14 / weekly |
| Claim escape | Material unsupported/altered claims found after S02 lock or downstream QA | NOT MEASURED | Zero serious escapes | S02 + S12 / continuous |
| Rights/privacy escape | Unauthorized asset/data exposure or missing required permission discovered downstream | NOT MEASURED | Zero serious incidents | Accountable owner / continuous |
| QA escape | Blocker/major defects discovered after S12 handoff or publication | NOT MEASURED | No increase; serious escape stops pilot | S12 / continuous |
| Misclassification | Independently adjudicated lane differs from assigned lane | NOT MEASURED | Set after shadow phase | Risk owner / weekly |
| Renderer fidelity | Contract cases mapped/runtime-tested without unapproved semantic loss ÷ cases tested | NOT MEASURED | Set after pinned smoke test | S10 + S12 / release |

Do not collapse these into one score. Report numerator, denominator, missingness, cohort size, uncertainty and defect severity.

## Study design
Phase 0: retrospective baseline from comparable cases if reliable. Phase 1: shadow mode; standard route remains authoritative and recommendations are independently adjudicated. Phase 2: limited R0/R1 controlled pilot only after written approval; R2/R3 excluded. Phase 3: independent process/usability/safety evaluation and accountable expansion decision.

No causal claim from simple before/after comparison. Document selection bias, case-mix changes, seasonality, learning effects, missing data and external wait time. Small samples support descriptive results, not statistical certainty.

## Stop / rollback
Immediately stop for serious health-claim escape, privacy/consent or rights incident, unauthorized publication, bypassed approval, critical continuity defect or false PASS from validator/control failure. Pause for sustained major QA defects, misclassification, untraceable outputs or missing logs. Revert to standard route, preserve evidence, notify owners and complete corrective action before restart.

## Governance
Pilot requires named sponsor and owner, S02/S12 concurrence, privacy/rights review, baseline plan, approved sample, rollback owner and written authorization. This document defines measures; it does not authorize the pilot.