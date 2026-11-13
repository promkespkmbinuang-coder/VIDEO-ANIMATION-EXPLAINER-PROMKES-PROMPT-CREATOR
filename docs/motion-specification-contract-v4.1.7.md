# V4.1.7 — Renderer-neutral Motion Specification Contract

**Status:** additive contract. It specifies intended motion and static validation; it does not prove that an AI model obeyed the prompt, that a renderer executed it, or that media passed inspection.

## 1. Ownership

| Domain | Owner | Authority |
|---|---|---|
| Shot/camera plan | S06 | Shot purpose, composition, lens/viewpoint, camera design and camera-move intent |
| Motion | S07 | Element states, key poses, path, timing, easing, anticipation/follow-through/settle |
| Still/reference prompts | S08 | Single-state visual reference prompts and asset linkage |
| Composition/renderer | S10 | Canonical-to-renderer mapping, transforms, frames, tracks, code and execution evidence |
| Independent QA | S12 | Static motion QA and conditional rendered-media QA |
| Continuity | S13 | MCG/Guide/scene state index, lock/dependency invalidation |
| Orchestration | M00 | Routing, gates, manifest integration and status aggregation |

No S15 is created. The existing ownership graph already has the required production responsibilities; the missing piece is a shared, testable motion contract and explicit handoffs.

## 2. Time and frame semantics

The canonical interval is **half-open**: \`start_frame\` is inclusive and \`end_frame_exclusive\` is exclusive.

\`duration_frames = end_frame_exclusive - start_frame\`

This avoids off-by-one ambiguity. Each record states \`fps\`, \`timebase\`, \`timing_source\`, \`source_precision\` and \`rounding_policy\`. Frame-accurate values require a known fps/timebase. S09 owns audio-derived timing and must preserve the actual source precision. A text-only script or inferred reading speed cannot be upgraded into exact audio sync.

Each animated element records stable IDs, initial/final state, ordered keyframes, interval, fps/timebase, timing source/precision, motion phases, path and coordinate system/unit, easing, negative constraints, continuity/claim/source refs, accessibility fallback and intended renderer targets.

## 3. Quantification rules

1. Replace vague terms (“smooth”, “dynamic”, “cinematic”) with observable values or measurable direction: position, scale, rotation, opacity, path, interval, hold, speed/range or bounded easing.
2. State units. Do not mix pixels, normalized coordinates, degrees, seconds and frames without conversion context.
3. Give each element a stable identity; separate subject/object/environment motion. Reference an S06 camera plan instead of inventing camera parameters in S07.
4. Cubic-bezier values require a renderer that supports that curve. Spring parameters require stiffness, damping and mass; they are not portable without a target adapter.
5. If a generative model exposes no deterministic curve/frame controls, translate intent into natural language and label numeric values as requested guidance, not executable controls.
6. A \`MODEL_LANGUAGE_ONLY\` easing record explains the desired motion in words; it does not imply exposed model controls.
7. Overlaps must be explicit; motion events must fit the available scene duration.
8. Aesthetic adjectives are not acceptance criteria.

## 4. Beat sheet and time-coded handoff

A beat sheet is an editing/communication table, not a replacement for the machine-readable motion record. Each beat maps to a scene/shot and includes \`beat_id\`, \`time_in/time_out\` and precision, optional frame range, narrative function, approved message/claim refs, S06 shot ref, S07 motion refs, S09 audio refs, transition ref, approved overlay refs and readability/hold note.

Do not enforce a generic “one movement every two seconds” rule. Movement density follows comprehension, narration, risk, accessibility, scene purpose and platform limits. A deliberate hold is valid when it improves reading or reflection.

## 5. Schema and renderer adapters

\`schemas/v4/motion-record.schema.json\` is the renderer-neutral source contract. \`scripts/validate_motion_contract.py\` validates its JSON Schema and semantic rules for:
- half-open interval arithmetic;
- keyframe order, uniqueness and range;
- phase bounds;
- easing parameter completeness;
- S09 timing precision/provenance;
- S06 camera-plan ownership;
- platform feature claims backed by evidence.

The canonical record is not a universal Remotion/GSAP/Lottie schema. S10 must produce a target-specific mapping and validate each adapter separately. Mapping loss, unsupported values and manual steps are explicit. \`renderer_targets\` means requested targets, not verified compatibility.

## 6. Evidence levels

- JSON Schema/static semantic validation proves only that the declared record conforms to the declared contract.
- Unit/contract tests prove only the tested cases in their test environment.
- Renderer integration tests prove only the exact mapping/runtime, version and configuration tested.
- Render QA requires an actual output artifact and observation/measurement.
- Clinical, institutional, legal, rights, privacy, brand, accessibility and release approvals remain independent human-controlled gates.

Static PASS cannot be promoted to runtime/render/media PASS. Missing evidence stays \`NOT_RUN\`, \`NOT_VERIFIED\`, \`BLOCKED\` or \`NOT_APPLICABLE\` with reason.
