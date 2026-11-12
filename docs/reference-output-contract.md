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
