# Remotion target mapping — V4.1.8

**Target selected for a concrete mapping design: Remotion (React composition renderer).**
**Execution status: NOT_RUN.** No package installation, Studio discovery, bundle, render, MP4 export, frame inspection or audio inspection was performed in this change. This document is a target-specific implementation contract, not a compatibility claim.

## Canonical-to-Remotion mapping

| Canonical source | Remotion concept | Mapping rule | Evidence required |
|---|---|---|---|
| Project composition settings | `Composition` | Explicit id, width, height, fps, durationInFrames | package lock + composition registry read-back |
| Scene/shot | `Sequence` | start frame and duration derived from half-open interval | scene/shot IDs and frame arithmetic test |
| Motion keyframes | React style/interpolation | Convert canonical units to pixel/normalized values; preserve easing intent and clamp policy | unit tests for boundary frames and supported easing |
| Camera plan | nested wrapper / transform layer | S06 remains author; S10 maps only | camera-plan ref + mapping review |
| Approved overlay | text/SVG/image layer | Use exact approved text/hash; never regenerate clinical text | overlay hash verification |
| Audio segment | audio component/track | Preserve source offset, trim and volume envelope; no invented sync | audio metadata + listening/sync QA |
| Transition | explicit overlap/transition component | overlap budget must fit composition; no hidden duration extension | transition bounds test |
| Accessibility | reduced-motion branch + captions/contrast | static or reduced-motion fallback; captions retain approved wording | accessibility inspection |
| Render artifact | output file | deterministic render command and recorded environment | actual output + S12 media QA |

## Mapping constraints

- Canonical data is renderer-neutral; Remotion code is generated/maintained by S10 only.
- Frame interval convention is `[start_frame, end_frame_exclusive)`. A Remotion sequence receives `durationInFrames = end - start`; the final occupied frame is `end - 1`.
- Do not infer fps, dimensions, codec, audio policy or Remotion version. They must be selected in a project profile and captured from the lockfile/runtime.
- Unsupported easing, spring, masks, blend modes, camera effects or audio controls must produce a mapping-loss record and a manual/fallback decision. Never silently approximate a safety-critical or message-critical effect.
- AI-generated footage is an asset input, not the renderer timeline itself. Model prompt output and Remotion deterministic composition are separate stages.
- Renderer adapter `DOCS_VERIFIED`, `STATIC_MAPPING_VALIDATED`, `RUNTIME_TESTED`, `RENDERED`, and `MEDIA_QA_VERIFIED` are distinct states; none implies the next.

## Minimal integration pilot

1. Pin Node, package manager, Remotion packages and exact versions in a disposable test project.
2. Build one non-clinical synthetic scene with one title overlay, one rectangle/object motion, one transition and one audio-free timing check.
3. Validate canonical input and produce a mapping-loss report.
4. Run typecheck/lint and boundary tests at frame 0, start−1, start, end−1 and end.
5. Run Remotion bundle/Studio discovery and render a short MP4.
6. Inspect metadata and every frame (or documented sampling protocol), then inspect playback, crop, text, flicker, continuity and audio absence.
7. S12 independently records observed results, defects and limitations. Preserve source, lockfile, command, environment, output hash and QA report.

No clinical material is used in this first technical smoke test. Passing it establishes only the exact pinned Remotion configuration tested—not general model or platform compatibility.
