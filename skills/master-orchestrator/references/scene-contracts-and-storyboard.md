# Scene and storyboard contract — reference-first

Every scene record is a reference contract for downstream composition, not a direct instruction to generate a complete video scene.

Required fields:
- `project_id`, `scene_id`, `scene_order`;
- target duration, start/end time, fps/timebase and frame range when known;
- story beat and key message/source fact references;
- shot ID, framing, viewpoint, composition, lighting and camera intent;
- character/environment/prop IDs and relevant MCG Guide/lock versions;
- still/keyframe `reference_id` values;
- motion reference IDs (key states, transforms, timing, easing intent) owned by S07;
- continuity-in/out and allowed variations;
- separate overlay/subtitle IDs containing exact approved text;
- audio cue IDs and timing references;
- transition/edit intent and open items.

## Reference prompt contract

S08 compiles each selected shot into a prompt for one still/reference image. The prompt describes a captured visual state, subject, pose, environment, composition, viewpoint, lighting, aspect ratio, relevant locks and negative constraints. It must not direct a video generator to render continuous footage or animate the full scene.

## Text rendering rule

Exact institutional text, health claims, numbers, dates, logos, contact information and CTA remain separate editable overlay data for the downstream composition system. Never rely on image-model typography for exact factual content.

## Timing rule

Scene time and frame ranges must be arithmetically consistent. Motion references are separate from static image prompts. If scene transitions overlap, state the overlap and account for it in total duration.

## Downstream renderer boundary

The contract is renderer-neutral. A Remotion or similar implementation must adapt the records to its own validated schema, register components/compositions, map actual reference asset files, implement motion/layers/text/audio and run render/artifact QA. This document is not executable renderer code.
