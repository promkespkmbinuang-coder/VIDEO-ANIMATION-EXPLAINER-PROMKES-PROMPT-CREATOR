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
# Output and Delivery Contract V2

## Output principle

The system returns the highest production level actually supported by supplied inputs, tools, permissions and evidence. It may deliver a creative/reference package, a renderer-ready project, a rendered media file or a partially verified render. Never imply a later stage has occurred because an earlier stage is complete.

## Primary outputs

1. Project brief, input mode, capability matrix and assumptions.
2. Source Material Dossier and source provenance.
3. Health Truth Registry, claim-evidence records, safe wording and Fact Locks.
4. Audience/Campaign Blueprint and approved CTA.
5. Story treatment, screenplay, verbatim source transcript and edited VO as separate artifacts.
6. MCG index, seven Guide registry, global locks and scene continuity ledger.
7. Storyboard, shot list, scene contracts and timing provenance.
8. Motion specification and renderer constraints.
9. Still/reference prompt pack and Reference Asset Manifest.
10. Audio Intelligence Report, transcript provenance, segment IDs, timing granularity and uncertainty log when audio is supplied/readable.
11. SRT/VTT and caption cues only where timing supports them; otherwise untimed/provisional captions.
12. Sound cue map, voice-first mix specification and actual processed audio only when a tool performs and verifies processing.
13. Renderer-neutral composition handoff and adapter/project files only when separately commissioned and supported.
14. Render settings/log, actual MP4 and verification report only when rendered.
15. Publication/accessibility package.
16. Dual QA report, defects, unresolved items, release recommendation and human approval state.

## Status semantics

- `DRAFT`: authored but not reviewed.
- `REVIEWED`: static/domain review completed.
- `REFERENCE_READY`: required reference package passes its acceptance gate.
- `RENDER_READY`: complete implementation handoff and requirements exist; no render is claimed.
- `RENDERED_PARTIALLY_VERIFIED`: file exists, but some material checks are not verified.
- `RENDERED_VERIFIED`: actual output file exists and all defined critical technical checks have evidence.
- `BLOCKED`: material content, source, authority, rights, capability or runtime blocker.

Stage-level states: `NOT_STARTED`, `IN_PROGRESS`, `READY_FOR_REVIEW`, `APPROVED`, `BLOCKED`, `FAILED`, `NOT_APPLICABLE`. `NOT_APPLICABLE` requires a reason.

## Asset lifecycle

`PROMPT_DRAFT → PROMPT_REVIEWED → GENERATION_PENDING → GENERATED → SELECTED → APPROVED → USED_IN_RENDER`

Each transition needs observable evidence. File placeholder is not a file. A generated asset is not automatically selected or approved. Rights status is separate from technical existence.

## Timing contract

Every segment, subtitle cue, scene and animation sync point records `timing_source` and `timing_granularity`: `word`, `phrase`, `segment`, `scene`, `estimated`, or `none`. Use exact-looking timestamps only when measured or supplied. Do not create word-level timing from reading speed. Scene-to-frame conversion requires declared fps, timebase and rounding convention.

## Human approval contract

Clinical/institutional factual approval, likeness/voice consent, copyright clearance and publication authorization are independent gates. A technical render can be `RENDERED_VERIFIED` while publication remains `PENDING`. Only the authorized human owner can approve those matters.
