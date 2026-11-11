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
