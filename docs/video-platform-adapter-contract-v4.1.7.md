# V4.1.7 — AI Video Platform Dialect Adapter Contract

**Purpose:** translate one approved, source-grounded creative brief into target-specific prompt dialects without claiming that different models share controls or behavior.

## 1. Candidate platform families

OpenAI Sora, Google Veo, Kling, Runway and Seedance are **candidate families, not a current support declaration**. An adapter is usable only for an exact provider/product/model/version and scoped task. Product-family names or legacy presets do not prove current capability or API availability.

## 2. Required adapter evidence

Use \`schemas/v4/video-platform-adapter.schema.json\`. Every record includes exact provider/model/version, check timestamp, status (\`NOT_CHECKED\`, \`DOCS_VERIFIED\`, \`RUNTIME_TESTED\`, \`UNAVAILABLE\`, \`DEPRECATED\`, \`BLOCKED\`), current official documentation refs, dialect language/structure/length guidance, reference-image/audio policy, feature matrix, runtime test refs/environment where applicable, limitations, fallback and review trigger.

Every \`SUPPORTED\`, \`UNSUPPORTED\` or \`CONDITIONAL\` feature requires evidence refs. \`UNKNOWN\` is the default when unverified.

\`DOCS_VERIFIED\` means official documentation was checked; it does not prove host execution. \`RUNTIME_TESTED\` requires reproducible test evidence for the exact model/version, input, configuration and environment.

## 3. Adapter workflow

1. Preserve canonical source intent and health/message locks.
2. Produce a provider-neutral scene instruction first.
3. Select one exact target model/version for an adapter pass.
4. Map supported controls; omit unsupported parameters or label them as manual direction.
5. Keep health text, dates, statistics, names, logos and CTA in verified editable overlays rather than model-generated typography.
6. Preserve negative constraints and continuity anchors. Adapters cannot rephrase S02-locked claims.
7. Record fields dropped, approximated, translated to natural language or requiring manual work.
8. Validate syntax/length only against the target’s current specification.
9. Test with a non-sensitive fixture where possible; retain prompt, response/artifact, model version, run metadata and inspection result.
10. Recheck when provider documentation, model version or UI/API behavior changes.

## 4. Adaptive nine-slot prompt anatomy

Use these slots proportionally; omit irrelevant fields with a reason rather than inventing detail.

1. **Subject & factual boundary:** subject/state and approved source/claim refs; no new health fact.
2. **Action/behavior:** one primary observable action per beat; objective and CTA remain source-locked.
3. **Setting & staging:** environment, subject placement and composition aligned with S05/S06.
4. **Camera intent:** reference S06 shot/camera plan; do not invent unsupported lens/camera controls.
5. **Motion arc:** initial state, action, anticipation/follow-through/settle and S07 references.
6. **Time & beat:** duration, shot/beat boundary and precision source; distinguish exact frames from estimated timing.
7. **Visual treatment:** approved style/material/light/color continuity from S05/MCG.
8. **Constraints & negatives:** no invented medical details, text distortion, logo drift, misleading visualization, unsafe behavior, stigma/fear manipulation or unwanted artifacts.
9. **Audio & accessibility:** S09 audio/VO intent plus subtitle/readability/reduced-motion requirements from S11/S12 as appropriate.

This is a completeness checklist, not permission to collapse still prompts, temporal video prompts, motion records and renderer code into one artifact.

## 5. Fail-closed adapter rules

- Unknown exact model/version: provider-neutral prompt only; adapter \`NOT_CHECKED\`.
- Inaccessible official docs: do not assert platform parameters.
- No guarantee of exact text, claim fidelity, continuity, timing or camera movement: move factual text to editable overlays and record limitations.
- Health, rights, consent, privacy or accessibility conflict: block the affected output, not the governance rule.
- Count supported adapters only at their evidence level; candidate names do not count.
