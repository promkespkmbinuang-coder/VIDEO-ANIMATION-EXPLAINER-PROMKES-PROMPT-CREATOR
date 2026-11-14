## 4.1.9 — governed reuse, drift review and risk-proportional preflight (2026-11-14)
- Adds JSON Schema and semantic validation for AFL, immutable MDS observations and human-accepted baselines, non-authoritative MSA, process-only POR and risk-proportional preflight.
- APPROVED formula requires clear rights, provenance, scope, test evidence, independent S12 QA and human approval bound to exact formula hash.
- Drift observations are separate from accepted baseline; failed fetch/parse/policy checks never mean no change. No scheduler or automatic baseline update is activated.
- S14 remains COMPLETE and mandatory in every lane; UNKNOWN material risk is at least R2; critical triggers force R3; R2/R3 never fast-track.
- New unit tests do not close the GitHub 45-case or private 20-case acceptance suites.
- PR #24 exact-head CI verified successful (120 pytest checks plus successful link check); PR #25 subsequently reverted it for an unknown reason. No release approval is inferred.
- External runtime, scheduled monitoring, renderer render, MP4/media QA, independent review and human release approvals remain NOT_RUN/NOT_VERIFIED/HOLD as applicable.

## 4.1.8 — R0–R3 risk routing, beat-sheet trace and Remotion target mapping (2026-11-13)
- Adds conservative R0 LOW, R1 STANDARD, R2 ELEVATED and R3 CRITICAL routing with unknown-risk escalation, hard overrides and stop/escalate controls.
- Adds executable risk and beat-sheet semantic validators, regression tests, a beat-sheet schema and example.
- Adds a Remotion target mapping design with explicit mapping-loss and evidence stages; runtime, bundle, render, MP4 inspection and media QA remain NOT_RUN.
- Adds KPI baseline and controlled-pilot evaluation protocol; baselines remain NOT_MEASURED and R0/R1 pilot remains PROPOSED/inactive.

## 4.1.7 — quantified motion, platform evidence and cinematic QA (2026-11-13)
- Adds a renderer-neutral S07 motion-record schema and semantic validator for half-open frame intervals, keyframes, phases, easing, paths, source precision and S06 camera references.
- Adds a version-pinned S08 platform adapter evidence schema and nine-slot prompt completeness model; platform candidates are not declared supported without exact documentation/runtime evidence.
- Extends S12 observable cinematic/motion QA inside existing QA layers; no S15 and no duplicate gate.
- Adds risk-proportional routing as a proposed low-risk pilot while preserving required evidence, rights/privacy/consent and human controls.
- Adds repository evaluation, roadmap and metric documentation. New unit tests remain separate from the existing scenario acceptance suites.

## 4.1.6 — canonical MCG integration (2026-11-13)
- Adds canonical MCG schema and DRAFT example, seven single-owner Guide files and three continuity protocols.
- Makes S13 the MCG index and GUIDE-07 integrator only; clarifies GUIDE-01/03/06 S05, GUIDE-02/04 S04, GUIDE-05 S09.
- Requires post-storyboard S13 refresh before S08 reference compilation.
- Adds semantic checks, adaptive continuity, S02 claim ownership and approval/hash-binding contracts.
- Adds 76-case traceability coverage; scenarios remain NOT_RUN.
- External AI, renderer, media QA and human approvals remain separate gates.

# Changelog

## 4.1.4 — context-oracle alignment and corrective regression fix (2026-11-12)
- Aligns distribution aspiration wording with the fail-closed regression oracle: reach/FYP/trending/engagement are not guaranteed.
- Adds no new production capability; preserves the 26-record context register, optional S11 scope and unchanged private CTRL engine.
- Records the V4.1.3 candidate CI result honestly (92 passed, 1 assertion failed) and supersedes its test result with a corrected patch candidate.
- Full private package test suite remains NOT_RUN; exact-head GitHub CI for V4.1.4 is required before review/merge.

## 4.1.3 — cross-domain conversation continuity and evidence hygiene (2026-11-12)
- Expands the bounded context register from 19 to 26 records, adding explicit static infographic dimensions, optional social distribution aspirations, figurative copywriting limits, campaign-scoped environmental CTA, style preferences, product/repository identity ambiguity and historical V3-test boundaries.
- Strengthens S11 optional captions/hashtags/platform packaging while prohibiting promises of reach, FYP, trending, virality or engagement.
- Strengthens S14/M00 cross-domain scope and source-to-release traceability; preserves project-specific facts and superseded event briefs.
- Adds a register-schema/uniqueness regression test and an explicit legacy-V3 test-ledger warning.
- Keeps private legacy CTRL engine separate from GitHub V4-CTL candidate; no unreviewed engine synchronization.
- Host, AI, Remotion render, media QA, rights/license and human approvals remain separate evidence; production remains HOLD.

## 4.1.2 — conversation context and parity correction
- Adds summary-bounded context register and mandatory M00/S14 preflight.
- Corrects S10 mapping as proposed; preserves both source paths.
- Separates private legacy CTRL engine from GitHub V4-CTL candidate.

## 4.1.8 — R0–R3 risk routing, beat-sheet trace and Remotion target mapping (2026-11-13)
- Operationalizes R0 LOW, R1 STANDARD, R2 ELEVATED and R3 CRITICAL risk routing with conservative max-lane logic, unknown-risk escalation, critical overrides and stop/escalate requirements.
- Adds executable risk-assessment and beat-sheet semantic validators with regression tests; validation is not clinical risk certification or release approval.
- Adds beat-sheet schema, example and source-to-message-to-scene/shot-to-motion/audio/overlay-to-QA trace contract.
- Adds a concrete Remotion mapping contract and status record; no runtime, bundle, render, MP4 inspection or media QA is claimed.
- Adds KPI baseline and controlled-pilot evaluation blueprint. Baselines are NOT MEASURED; R0/R1 pilot remains PROPOSED, inactive and approval-gated.
