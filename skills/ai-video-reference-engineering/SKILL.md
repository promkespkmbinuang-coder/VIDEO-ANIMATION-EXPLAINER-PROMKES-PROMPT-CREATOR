---
name: ai-video-reference-engineering
description: Use when compiling renderer-neutral image/reference prompts and structured visual-production references for later composition in Remotion or a similar rendering system; never generate direct text-to-video prompts or claim to render video.
---

# S08 — AI Visual Reference Prompt Engineering

## Mission

Transform the approved screenplay, storyboard, visual canon, character/environment Guides, and motion/editing references into a **Reference Prompt Pack**. The pack is a source of visual assets and structured production references that a downstream renderer such as Remotion can assemble. It is not a prompt-to-video package and is not a video-rendering implementation.

## Non-negotiable output boundary

S08 creates prompts for still/reference assets and structured reference data only. Do not write instructions asking a text-to-video model to generate a finished moving scene, continuous video, or complete video sequence. Do not claim video generation, rendering, encoding, or export.

Allowed reference prompt types:
- master visual-language / style reference;
- character model sheet, expression sheet, wardrobe and pose references;
- environment/background plate and prop/object references;
- scene keyframe or shot reference stills;
- visual state references (start, key pose, end pose) when useful;
- isolated transparent assets or overlay artwork references when supported by the selected image tool.

The prompts describe **what reference image/asset should exist**, not how a video generator should animate an entire scene. Motion is represented separately by S07's timing and transform references. Camera framing and shot intent are represented by S06. Edit timing and layers are represented by S10.

## Ownership

**Owns:** reference asset prompt compiler; prompt-to-reference blocks; reference asset variants; renderer-neutral asset IDs and manifest; reference prompt capability notes for image/reference generators; consistency requirements linking references to MCG locks.

**Does not own:** health fact approval (S02); campaign strategy or screenplay (S03/S04); visual canon (S05); shot design (S06); motion values/timing (S07); renderer implementation/code or rendering (S10/downstream team); final QA/release disposition (S12/M00).

## Inputs

- S01 source dossier and source asset IDs;
- S02 Health Truth Registry / fact locks;
- S04 approved story and screenplay;
- S05 visual identity, character, style, environment and prop canon;
- S06 storyboard, shot list, framing and camera reference;
- S07 motion design references (timing, transforms, easing intent, state transitions);
- S13 MCG, Guide IDs/versions, lock registry and scene continuity ledger;
- optional image-reference platform/model and its verified capabilities.

If an input is absent, continue only with labelled placeholders or mark the dependent reference `BLOCKED`. Do not fabricate canon or claim external model support without checking it.

## Workflow

1. **Read the locks:** collect project ID, MCG version, character/style/environment IDs, source facts that must remain visible, and scene IDs. Resolve conflicts through M00; do not choose a conflicting design silently.
2. **Choose reference depth:** `LITE` (one style reference + key reference stills), `STANDARD` (character sheets, environment plates, prop references and scene keyframes), or `ADVANCED` (multi-episode reusable asset library, variants, state references and change-impact map).
3. **Define the reference inventory:** assign stable `ASSET-REF-ID` values, asset type, owner, canonical Guide/lock version, scene usage, required aspect ratio, composition, transparency needs, and delivery status.
4. **Compile the master reference prompt:** state art direction, medium, palette, shape language, texture, light, rendering treatment, composition rules, and prohibited drift. Treat the accepted S05 Guide as authoritative.
5. **Compile character/environment/object reference prompts:** include immutable identity details, neutral turnaround/expression/pose needs, environment layout, prop relationships, visual scale, and allowed variations. Never infer private or sensitive personal attributes from a photo.
6. **Compile scene keyframe/reference prompts:** each prompt is standalone and includes the selected scene/shot, subject, pose/action snapshot, environment, composition, camera viewpoint as a still-image reference, lighting, palette, aspect ratio, crop/safe area, relevant lock IDs/versions, and negative constraints.
7. **Separate text from image references:** exact dates, health claims, institutional names, logos, phone numbers, and CTA are supplied as verified overlay data for the downstream renderer, not entrusted to image-model typography.
8. **Separate motion from image prompting:** S07 supplies motion/state specifications. Do not bury movement instructions inside the image prompt other than describing a single captured pose or state.
9. **Build the renderer-neutral reference manifest:** use asset IDs, scene references, timing references, layer roles, order, source/license/consent status, and file placeholders. Do not output TSX, Remotion components, rendering commands, or renderer-specific implementation unless separately requested as a different task.
10. **Validate and hand off:** inspect prompt completeness, lock compliance, asset linkage and capability honesty; route defects to S05/S06/S07/S13 as appropriate; send the pack to S10 and S12.

## Reference Prompt Contract

Each prompt record must contain:
- `reference_id`;
- `reference_type` (`STYLE`, `CHARACTER`, `EXPRESSION`, `POSE`, `ENVIRONMENT`, `PROP`, `SCENE_KEYFRAME`, `OVERLAY_ART`, `OTHER`);
- `project_id` and `scene_id` where applicable;
- `prompt` (positive description for one still/reference asset);
- `negative_constraints` (things that must not change or appear);
- `aspect_ratio` and target dimensions or `UNKNOWN`;
- `character_ids`, `environment_id`, `prop_ids` as applicable;
- `guide_ids` and `lock_versions`;
- `source_fact_refs` where factual content is visually represented;
- `allowed_variations`;
- `status` (`DRAFT`, `REVIEWED`, `LOCKED`, `BLOCKED`, `NOT_APPLICABLE`).

The manifest must distinguish reference prompt, generated reference asset, selected/approved asset, and missing asset. A prompt is not an image; a reference image is not a rendered video.

## Handoff to Remotion or similar renderers

S08 supplies renderer-neutral references and IDs. S10 may describe a mapping to downstream renderer concepts such as composition, scene/sequence, layer, asset path, frame range, transform, opacity, z-order, transition and audio cue. Remotion's `Composition` and input-props workflow can consume structured, JSON-serializable data, but this plugin does not produce or execute the React composition or invoke Remotion by default. Any Remotion-specific adapter/code is a separately scoped implementation task and must be based on the target project's schema and version.

## Output

1. Master Visual Reference Prompt.
2. Character / Expression / Pose Reference Prompts.
3. Environment and Prop Reference Prompts.
4. Scene Keyframe / Shot Reference Prompts.
5. Reference Asset Manifest (stable IDs and status).
6. Renderer-Neutral Reference Handoff (scene-to-asset mapping, timing/layer references, overlay/audio references).
7. Image-model capability notes and limitations.
8. Open items and handoff receipt.

## Quality gate

PASS only when reference prompts are still/reference-specific (not text-to-video directions), every reference is traceable to the right Guide/version, source facts remain locked, exact text is separated as overlay data, assets are not claimed generated/approved unless observed, and the handoff can be interpreted without inventing renderer code. Otherwise use `PASS_WITH_CAVEATS`, `HOLD`, or `BLOCKED`.
