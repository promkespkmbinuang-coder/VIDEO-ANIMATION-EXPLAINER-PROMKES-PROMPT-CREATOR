# Production workflow — Prompt-to-Reference

1. **Source intake:** S01 extracts poster, caption, facts, brand cues and source assets.
2. **Health truth lock:** S02 verifies/labels claims and locks approved wording.
3. **Campaign brief:** S03 sets audience, objective, behavior and CTA.
4. **Story/script:** S04 creates treatment, screenplay, dialogue and VO timing.
5. **Canonical Guides:** S05 authors visual canon; S13 maintains MCG and seven Guide modules.
6. **Storyboard/shot references:** S06 creates scenes, shots, composition and viewpoint.
7. **Motion reference data:** S07 defines key states, transforms, motion path and timing as structured references, not generator commands.
8. **Prompt-to-reference:** S08 creates master style, character, environment, prop and scene-keyframe still/reference prompts with stable IDs.
9. **Audio references:** S09 supplies VO performance, cue sheet, music direction and sound timing.
10. **Renderer-neutral handoff:** S10 maps approved assets, scene timing, layers, overlays, subtitles and audio into structured composition references.
11. **Distribution/accessibility:** S11 prepares captions, titles, subtitles/alt text and channel notes.
12. **Independent reference QA:** S12 checks facts, reference prompts, Guide locks, scene/timing math, assets and renderer handoff.
13. **Integration and human review:** M00 assembles one handoff and identifies human approvals.

## Rendering boundary

The final video is rendered downstream in Remotion or a comparable composition/rendering system. This plugin does not create a final video, direct text-to-video prompts, Remotion TSX components or run render commands by default. A separately commissioned renderer implementation must define the target project schema, assets, components, environment, permissions and render/artifact acceptance tests.
# Production Workflow V2

## Stage 0 — Intake and capability discovery

Determine `POSTER_FIRST`, `AUDIO_FIRST`, `HYBRID` or `SCRIPT_FIRST`. Inspect all supplied files before asking follow-up questions. Capture project objective, audience, language, platform, duration, canvas, aspect ratio, fps, brand and rights constraints. Check each capability independently: image/file read, audio decode, metadata, ASR, transcript alignment, diarization, acoustic inspection, audio processing, image/reference generation, code execution, renderer, export and media inspection. Record evidence and `VERIFIED`, `UNAVAILABLE`, `NOT_TESTED` or `NOT_APPLICABLE`.

## Stage 1 — Source and audio intake

S01 extracts literal poster/caption/script information, brand cues, unreadable regions and contradictions. S09 inspects accessible audio, verified metadata, transcript provenance, source-to-transcript differences, segment IDs, speaker IDs only when grounded, timing granularity and uncertainty. When either input family is absent, mark it `NOT_PROVIDED`; never invent it.

## Stage 2 — Health truth and fact lock

S02 atomizes all material health claims originating from poster, caption, script or audio. Verify current applicability and evidence where accessible. Distinguish source claim, verified claim, inference, creative metaphor, contested claim and unknown. Lock only safe/approved wording. An unverified material claim remains `BELUM DIVERIFIKASI` and may block affected factual scenes/overlays.

## Stage 3 — Campaign and narrative

S03 defines one primary audience, objective, behavior, barrier, key message and CTA. S04 builds treatment, screenplay, dialogue and VO. Preserve original supplied VO separately from edited/adapted script. Every factual statement maps to the Health Truth Registry.

## Stage 4 — Visual canon and continuity

S05 authors style, design tokens, typography, character, environment and prop canon. S13 registers MCG and seven Guides, canonical locks, scene states, versions and change impact. Never treat a proposed style as an approved brand rule.

## Stage 5 — Storyboard and motion

S06 maps semantic scenes/shots to source transcript segment IDs and measured or clearly labeled estimated timing. Scene durations must reconcile to the chosen target/runtime; do not cut syllables or hide overruns. S07 specifies element states, trigger/synchronization source, path, transform, easing, duration, hold, exit, transition and renderer fallback. Motion timing precision cannot exceed the source timing precision.

## Stage 6 — Reference assets

S08 compiles still/reference prompts and manifests for style, characters, expressions, poses, environment, props and scene keyframes. Exact medical wording, institutional names, dates, numbers, logos and CTAs remain separate editable overlay data. A prompt is not an asset; generated, selected and approved are different states.

## Stage 7 — Audio post and subtitles

S09 creates verbatim captions from the preserved transcript and SRT/VTT only when timestamps are supportable. Prepare sound cue mapping, voice-first mix, ducking, fades, rights notes and measurable checks. Processing instructions are not completed processing; actual audio edits require a capable tool and verification.

## Stage 8 — Composition, renderer integration and export

S10 maps approved scenes/assets/motion/overlays/subtitles/audio to a renderer-neutral composition contract. Test renderer, dependencies, fonts, codecs, file access, permissions and export separately. Choose native, programmatic or handoff route. Render a proof segment when feasible, inspect it, then attempt the full render. Do not install packages, transmit private assets or use paid/external services without authorization.

## Stage 9 — Dual QA

S12 performs content/reference QA and, only when actual output exists and can be inspected, artifact QA. Check health fidelity, script-to-scene trace, MCG continuity, reference completeness, timing, subtitles, audio, rights, accessibility, dimensions, fps, streams, duration, opening, visual defects, blank frames and A/V sync according to available tools. Uninspected properties remain `NOT_VERIFIED`.

## Stage 10 — Delivery and correction

M00 aggregates each stage and returns one accurate delivery state. Route defects to the narrowest owner. Changes propagate through the invalidation map; rerun affected tests plus regression checks. Technical QA pass does not equal clinical sign-off or publication authorization.
