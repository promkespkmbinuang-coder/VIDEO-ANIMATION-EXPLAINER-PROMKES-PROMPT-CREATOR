# Prompt-to-Reference Output Contract

## Purpose

The plugin produces prompts and structured references for visual assets and later programmatic composition. It does **not** produce a final video and does not provide text-to-video prompts by default.

## Deliverable boundary

### Produced by this plugin
- Still-image/reference prompts for style, character sheets, poses, expressions, environments, props and scene keyframes.
- Storyboard, shot and camera-framing references.
- Motion/timing reference data (key states, transforms, easing intent, frame/time ranges).
- VO, sound and overlay/subtitle reference sheets.
- Reference Asset Manifest with stable IDs, status and paths/placeholders.
- Renderer-neutral composition handoff that maps scenes to references, layers, time ranges, overlays and audio cues.

### Not produced by default
- Text-to-video prompts directing a generator to create continuous finished footage.
- Final MP4/MOV, rendered frames, audio mixes or encoded deliverables.
- React/TSX Remotion composition code, renderer project scaffold, CLI commands or deployment configuration.
- Claims that reference assets were generated, selected, approved or rendered without evidence.

A separate request may commission a renderer implementation or actual render, with explicit scope, target environment, permissions and acceptance tests.

## Reference Prompt record

| Field | Type | Meaning |
|---|---|---|
| reference_id | string | Stable asset-reference identifier |
| reference_type | enum | STYLE, CHARACTER, EXPRESSION, POSE, ENVIRONMENT, PROP, SCENE_KEYFRAME, OVERLAY_ART, OTHER |
| project_id | string | Project identifier |
| scene_id | string/null | Scene when applicable |
| prompt | string | Prompt for one still/reference asset |
| negative_constraints | string[] | Forbidden drift/content |
| aspect_ratio | string/UNKNOWN | Required still aspect ratio |
| dimensions | object/UNKNOWN | Width and height reference |
| character_ids | string[] | Linked canonical characters |
| environment_id | string/null | Linked environment |
| prop_ids | string[] | Linked props |
| guide_refs | object[] | Guide ID and version |
| lock_refs | string[] | Applicable canonical locks |
| source_fact_refs | string[] | Facts represented visually |
| allowed_variations | string[] | Explicitly allowed variation |
| status | enum | DRAFT, REVIEWED, LOCKED, BLOCKED, NOT_APPLICABLE |

## Reference asset lifecycle

`PROMPT_DRAFT → PROMPT_REVIEWED → REFERENCE_GENERATION_PENDING → REFERENCE_CREATED → REFERENCE_SELECTED → REFERENCE_APPROVED`

Only transition a state when corresponding evidence exists. Generated and approved are not synonyms. Missing asset remains `MISSING`; proposed file path remains a placeholder.

## Renderer-neutral scene record

Each scene may specify:
- scene_id, scene_order, start_time, end_time, duration;
- start_frame, end_frame, fps and timebase where known;
- storyboard/shot reference IDs;
- reference asset IDs and path placeholders;
- layer role, z-order, transform, opacity, crop and safe-area notes;
- motion reference IDs and state transitions;
- overlay/subtitle record IDs and exact approved text;
- audio cue IDs and timing;
- continuity-in/out and Guide/lock versions;
- open implementation decisions.

This schema is reference data, not executable Remotion code. It must be adapted to the target project's validated input schema before rendering.

## Remotion mapping note

Remotion compositions can receive JSON-serializable input props and define metadata such as width, height, fps and duration. This allows a downstream Remotion project to map this handoff into its own composition schema. The plugin does not assume that a generic manifest automatically works as Remotion props; project-specific TypeScript/Zod schemas, components, asset loading and rendering setup must be supplied by the downstream implementation.

Official documentation: [Passing props to a composition](https://www.remotion.dev/docs/passing-props), [Composition](https://www.remotion.dev/docs/composition), [Parameterized videos](https://www.remotion.dev/docs/parameterized-rendering), [Render your video](https://www.remotion.dev/docs/render).
