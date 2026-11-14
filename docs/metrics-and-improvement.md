# Evaluation metrics and continuous improvement

Establish a measured pilot baseline before setting numerical targets. Every metric must state the denominator, measurement window, version/host/model, evidence source and whether it is static or dynamic.

| Dimension | Candidate indicator | Operational definition / caution |
|---|---|---|
| Health integrity | Material claim evidence coverage | Claims with recorded status, source locator, publication date and scope divided by all material claims; coverage is not proof every claim is true |
| Source fidelity | Source-fact preservation defects | Unapproved changes to dates, numbers, location, CTA, institution identity or health facts |
| Reference completeness | Required reference coverage | Required style/character/environment/prop/keyframe reference IDs resolved or explicitly marked N/A/blocked |
| Canon continuity | Guide/lock compliance | References and scenes linked to compatible canonical versions |
| Character continuity | Character continuity defect rate | Observed face, body, outfit, proportions or identity drift per comparable scene/asset set; requires actual generated references or renders |
| Change control | Change propagation accuracy | Correct dependent Guides, scenes, reference prompts and assets identified after a canonical change |
| First-pass acceptance | First-pass acceptance rate | Items accepted on first QA review divided by items reviewed, by output type and release |
| Regression | Regression pass/fail rate | Executed comparable tests; `NOT_RUN` and `BLOCKED` shown separately and excluded from pass denominator |
| Portability | Cross-platform invocation reliability | Successful discovery/invocation/reference-load/handoff runs divided by executed attempts per named host/version |
| Production efficiency | Rework rate | Reference/scene records revised due to preventable specification defects |
| Cross-modal integrity | Cross-modal mismatch rate | Actual visual/VO/subtitle/audio/overlay mismatches per inspected rendered artifact |
| Renderer handoff | Unresolved mapping defects | Missing/invalid asset IDs, frame ranges, layers, overlays or audio cue links |
| Artifact quality | Render defect rate | Defects observed in actual rendered output; requires actual render assets and inspection |

The previous six dashboard dimensions remain useful grouping headings, but counts per dimension are not quality scores. The indicators above should be populated from pilot observations; no percentage target is asserted before a representative baseline exists.

Collect only authorized and minimized feedback. The plugin does not imply self-learning, persistent telemetry or automatic renderer monitoring.


## V4.1.9 process-only outcome register

The Project Outcome Register is descriptive process measurement, not a clinical or audience-impact system. Allowed measures: cycle time, reviewer effort, rework rate, first-pass acceptance, approved formula reuse rate, stale-evidence detection latency, trace completeness, risk misclassification and QA escape count.

Each observation requires a defined cohort, reporting window, numerator, denominator, unit, missing count, evidence reference and limitations. A rate is undefined when its denominator is zero. Report counts alongside rates; stratify by risk lane and artifact class where sample size permits, but never average away an R2/R3 critical trigger.

No baseline, target, improvement percentage or causal effect is asserted before a measured cohort exists. Do not collect new audience/patient behavioral-health data, infer clinical effects or import analytics not supplied for the project. Small cohorts, survivorship, missing records, changing case mix and reviewer learning remain explicit limitations.
