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


## V4.1.9 — reuse and drift metrics

Add only after a project-local record and privacy review exist:
- Approved reuse ratio = APPROVED ledger references reused / eligible formula lookups.
- Reuse acceptance = reused formulas accepted without material rework / reused formulas reviewed.
- Drift detection latency = time from sourced provider change evidence to candidate event; it does not prove materiality.
- Stale evidence detection = stale/unknown adapter records found / records reviewed.
- Reviewer effort and median/P90 cycle time, stratified by risk lane and complexity.
- Rework, trace completeness, risk misclassification and major/critical QA escape.

Every metric requires a numerator, denominator, cohort, time window, version/host/model, evidence locator, missingness, owner and caveat. Do not create one composite score. Baselines remain NOT_MEASURED until a representative cohort is approved. Collect only privacy-minimized process data; do not collect new patient/audience behavioral-health data or infer clinical outcomes.
