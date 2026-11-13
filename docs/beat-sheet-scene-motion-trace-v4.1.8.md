# Beat-sheet and scene-to-motion trace — V4.1.8

**Status: CONTRACT + EXAMPLE IMPLEMENTED; integration into a live project remains NOT_RUN.**

## Purpose and ownership

A beat is the smallest meaningful narrative/communication unit. S04 owns narrative intent; S06 owns scene/shot/camera; S07 owns per-element motion; S09 owns audio/transcript timing provenance; S10 owns assembly and renderer mapping; S13 owns integrated scene continuity; S12 independently checks the joined trace. M00 owns the manifest and gate arbitration. No owner may author another domain's canonical fields.

## Required trace chain

`source_id / claim_id → message_id → beat_id → scene_id → shot_id → motion_id + element_id → audio_segment_id → overlay_id → transition_id → renderer_layer_id → QA criterion / evidence`

Every link must resolve or have an explicit `NOT_APPLICABLE` reason. No unlinked factual overlay, no motion without a scene/element owner, no renderer layer without canonical source record. Claim text remains S02-owned; never copy-edit or visually embellish a locked claim.

## Beat-sheet minimum fields

- Stable `beat_id`, sequence, `time_in/time_out`, timing precision/source and optional frame interval.
- Narrative function, audience state/desired comprehension, message/claim references.
- Scene/shot references, S06 camera-plan reference.
- S07 motion record IDs and element IDs; motion purpose and expected visual state.
- S09 audio segment reference, transcript/source precision, speaker only if grounded.
- Overlay IDs, exact approved text hash/reference, reading hold and safe-area constraints.
- Transition in/out, MCG state in/out and continuity lock version.
- Accessibility alternative (reduced motion, captions/alt text, contrast/readability).
- QA oracle: expected observable result, method, status, evidence ref and limitation.

## Timing

Time intervals are half-open: `[time_in, time_out)`. Frame intervals use inclusive start and exclusive end. Never derive frame-exact sync from script-only estimates. Each beat must identify `EXACT_AUDIO`, `SOURCE_TIMECODE`, `ESTIMATED` or `UNSPECIFIED`; estimated timing remains estimated through every downstream record. A deliberate hold is a valid beat. Do not impose arbitrary movement frequency.

## Example (illustrative only)

| Beat | Time | Purpose | Scene / shot | Motion | Audio / overlay | QA oracle |
|---|---|---|---|---|---|---|
| B01 | 0–3.5s ESTIMATED | Establish context | SC01 / SH01 | MOT01: title fades from opacity 0→1 over 12 frames; target renderer mapping pending | AUD01 narration ref; OVL01 approved title hash | Title legible; no factual assertion added |
| B02 | 3.5–8s ESTIMATED | Explain one action | SC02 / SH02 | MOT02: object enters from x=−120px to x=240px; hold 24 frames | AUD02 segment ref; OVL02 exact approved instruction | Action readable; instruction matches S02 Fact Lock |
| B03 | 8–10s ESTIMATED | Reinforce / pause | SC02 / SH03 | MOT03: static hold; no movement | AUD03 pause; OVL02 remains unchanged | Reading time sufficient; reduced-motion equivalent is static |

Example values are not production facts, validated timings or Remotion test evidence.

## Completion and invalidation

Beat-sheet completion requires 100% trace resolution or justified N/A, no dangling IDs, timing provenance consistency, approved overlay hashes, MCG continuity state, and S12 oracle coverage. A changed claim, source, VO timing, shot, motion, overlay, asset, renderer target or scene order invalidates only the transitive dependent records—but all invalidated QA and approvals must be rerun/rebound to the new hashes.

See `schemas/v4/beat-sheet.schema.json` and `scripts/validate_beat_sheet.py`.
