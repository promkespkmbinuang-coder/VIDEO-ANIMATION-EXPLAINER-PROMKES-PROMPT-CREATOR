---
name: editing-postproduction
description: Use when approved Promkes storyboard, assets, motion, audio and subtitles need composition, renderer integration, project assembly, conditional rendering, export or renderer-ready handoff.
---

# S10 — Editing, Post-Production, Renderer & Code Engineering

## Mission and ownership

Own the path from approved renderer-neutral scene/asset/audio/overlay specifications to a validated renderer adapter, assembled project and actual export when the exact host/runtime supports it. Preserve S02 health locks, S05/S13 visual canon, S06 shot decisions, S07 motion values and S09 audio/timing evidence. Do not claim renderer availability or export from a manifest alone.

## Single-owner responsibility lanes

S10 combines two complementary lanes under one owner:

1. **Editing and post-production:** editorial assembly, scene sequencing, pacing, transitions, overlays, titles, captions, subtitle integration, audio mix/ducking/loudness, synchronization, color/visual finishing, mastering and export preparation where the actual tools support them.
2. **Renderer and code engineering:** renderer-neutral composition contract, target adapter, source code, typed input mapping, project assembly, runtime checks, render orchestration and export verification.

S09 remains the owner of source-audio intelligence, transcript provenance, speaker/timing analysis, VO direction and sound-design specifications. S10 owns placing/processing those approved elements in the final timeline. S11 owns accessibility/distribution requirements; S12 independently verifies results. This division prevents duplicate authority and preserves both historical S10 scopes.

## Inputs

Approved production manifest; S06 scene/shot plan; S07 motion specs; S08 reference asset manifest; S09 source audio, transcript, subtitle cues and sound design; S11 accessibility/overlay requirements; user render target and permissions.

## Capability readiness

Check independently: file access; code execution; renderer availability/version; dependency presence; fonts; image/video/audio decoders; codec/container support; available memory/runtime; export destination; and media inspection. Status each `VERIFIED`, `UNAVAILABLE`, `NOT_TESTED`, or `NOT_APPLICABLE` with evidence. Do not infer capabilities from product branding or another session.

## Route selection

- `NATIVE`: an accessible native motion/video workflow can produce the required composition and export.
- `PROGRAMMATIC`: an accessible authorized renderer/runtime (for example Remotion, FFmpeg or another proven route) can assemble the manifest and media.
- `HANDOFF`: no usable renderer in the current environment; produce a renderer-neutral, implementable handoff and explicitly state no MP4 was created.
- `NONE`: rendering is not part of the user's requested scope.

Do not assume that a model-generated short clip is a deterministic multi-scene timeline renderer. Do not assume generic manifest JSON is automatically valid Remotion props or TSX.

## Editorial and post-production contract

Record edit decision/version, scene order, source segment IDs, in/out points, frame-accurate duration, transitions, overlays, captions, subtitles, audio cues, mix settings, loudness target (only when a standard is supplied), color treatment, graphics, safe areas and rights status. Keep supplied VO, edited VO, transcript, subtitles and final mixed audio as distinct artifacts with hashes and provenance. Do not rewrite clinically approved wording during editing. Unsupported transitions, effects, audio operations or codecs must be declared unavailable or handed off, never silently omitted.

## Composition contract

Create a deterministic mapping for project dimensions, aspect ratio, fps, timebase, total duration, ordered scene ranges, source segment IDs, reference asset IDs, asset paths/status, layer roles/z-order, transforms, crop/safe areas, transitions, overlays, captions, VO/music/SFX cues and rights. Exact health text, dates, statistics, institutional names, logos and CTA remain separate editable overlays. Use the manifest as one source of truth; never duplicate conflicting timestamps.

Frame conversion requires declared fps and rounding rule. Scene ranges must be contiguous or explicitly describe holds/overlaps/transitions. Every missing asset/path remains a placeholder or `MISSING`.

## Renderer/code engineering lane

Keep the renderer-neutral manifest separate from target-specific props and source code. Validate schema, asset IDs, path containment, exact renderer/version, dependencies, fonts, codecs, permissions and output destination before generating or executing an adapter. Mark generated code, static checks, integration, runtime, render, export and artifact inspection as separate evidence states.

## Render workflow

1. Validate manifest, IDs, required fields, scene/frame arithmetic and asset references.
2. Confirm critical assets exist and rights are sufficiently clear for the intended use.
3. Validate fonts, safe areas, alpha, overlays, subtitle cues, audio cues and renderer support.
4. Assemble using the selected route; preserve original audio and asset references.
5. Generate a short/low-resolution proof render when feasible.
6. Inspect proof for crop, legibility, continuity, timing, missing assets, A/V sync and audio intelligibility.
7. Correct observed defects with a recorded change ID; retry a failed render no more than once after a specific evidence-based correction unless a new explicit plan is approved.
8. Execute full export only after required proof gates pass.
9. Verify actual file existence, openability, container, dimensions, frame rate, duration, video/audio streams and sync to the extent tools permit.
10. Capture exact render route, versions, settings, output path/attachment ID, logs and remaining unverified checks.

## Output contract

- `capability_matrix`;
- `renderer_route` and exact verified tool/runtime/version;
- `adapter_status` and project/schema mapping;
- `composition_manifest_ref`;
- `project_artifacts` and asset/path status;
- `render_settings`;
- `proof_render_status`;
- `render_log` or exact failure classification;
- `actual_output_file` only when it exists;
- `verification_report` with per-check evidence;
- delivery state: `BLUEPRINT_ONLY`, `REFERENCE_READY`, `RENDER_READY`, `RENDERED_PARTIALLY_VERIFIED`, `RENDERED_VERIFIED`, or `BLOCKED`.

## Stop conditions

Never invent commands, dependencies, APIs, codecs, file paths or export URLs. Do not install packages or transmit private media without authorization. If renderer unavailable, stop at handoff. A project/code file is not an MP4. A present MP4 is not verified until inspected. Missing critical assets, broken audio, invalid timing, rights issues or failed proof checks block publish-ready export.


## V4.1.7 canonical motion adapter mapping

S10 consumes S07 canonical motion records and maps them to an exact renderer and version. Remotion, GSAP, Lottie and HyperFrames are not interchangeable schemas. Record each field as MAPPED, APPROXIMATED, QUANTIZED, OMITTED or MANUAL, with reason and fallback. Validate half-open frame ranges, fps/timebase conversion, element/track IDs, easing/path support, overlay/audio synchronization and asset references before execution.

A valid canonical motion record is not a renderer-runtime PASS. Actual integration, proof render, export and S12 inspection remain separate evidence stages. Do not silently convert unsupported motion controls or change health text to fit renderer limitations.


## V4.1.8 Remotion target adapter contract

Remotion is the first concrete target selected for a deterministic renderer mapping design. S10 maps canonical composition settings to Composition, scenes/shots to Sequence ranges, S07 keyframes to supported React interpolation/style transforms, S06 camera plan to composition layers, approved overlays to exact-text layers, S09 audio refs to timeline audio elements, and accessibility requirements to reduced-motion/caption alternatives. Preserve half-open frame arithmetic and report every unsupported/approximated/quantized/manual mapping. Pin exact Node/package versions before runtime testing. Current adapter status is DESIGN_ONLY_NOT_RUN: no install, typecheck, bundle, render, MP4 export or media QA has been executed. See docs/remotion-target-mapping-v4.1.8.md.

## V4.1.11 Remotion pattern mapping

For Remotion-targeted assembly, consult `../animation-motion-design/references/remotion-pattern-adoption-v4.1.11.md`. Check the exact runtime and adapter feature profile before mapping any pattern. Preserve unsupported features as mapping loss or fail-closed handoff. Distinguish composition-frame inspection from encoded-MP4 inspection; a source still is not encoded-media QA.
