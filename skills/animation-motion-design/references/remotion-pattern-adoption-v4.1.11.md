# Remotion Motion-Pattern Adoption Contract — V4.1.11

**Status:** additive, renderer-neutral motion-pattern catalogue and Remotion-specific mapping guidance. **Owner:** S07 for motion intent; S10 for renderer mapping and execution; S12 for independent QA; S05/S06/S09/S13 retain their existing domains.

This reference adapts useful design patterns observed in the public `haidrrrry/claude-remotion-skill` repository. It does not copy its hard rules as universal Promkes policy, does not add a new specialist, and does not claim that all patterns are supported by the current Promkes Remotion adapter.

## 1. Purpose and boundaries

Use the catalogue to help S07 select and specify an appropriate motion treatment for a scene. A pattern is a reusable design option, not a mandatory style or a substitute for the approved brief, storyboard, motion record, MCG, Health Truth Registry, accessibility requirements, or renderer capability evidence.

- S02 exclusively owns health claims, safe wording, evidence interpretation and Fact Lock.
- S05 owns visual canon, palette, typography and art direction.
- S06 owns framing, shot design and camera intent.
- S07 owns element motion, easing intent, keyframes, timing and transition-motion specification.
- S09 owns audio sources, transcript provenance, timing precision, voice and sound cues.
- S10 owns Remotion/renderer-specific mapping, code, runtime, rendering and export evidence.
- S11 owns accessibility and distribution requirements.
- S12 independently checks the specification and, only when actual media exists, the rendered result.
- S13 owns MCG indexing, Guide/lock references, scene-in/out continuity and change invalidation.

A style rule must not rewrite a medical claim, manufacture a timing value, change an approved character or logo, create a new camera move, or bypass rights/consent review.

## 2. Pattern catalogue

Patterns may be combined only when their interaction is intentional, technically supported and readable. Select the minimum set that serves the beat.

| Pattern ID | Pattern | Suitable use | Required caution |
|---|---|---|---|
| RMP-01 | Multi-property entrance | Introduce a subject or title with coordinated opacity, position and scale | Avoid automatic bounce or excess movement; respect reduced-motion needs |
| RMP-02 | Staggered choreography | Reveal a list, process steps or distinct visual elements in a meaningful order | Do not delay critical instructions or imply a false sequence |
| RMP-03 | Word/phrase reveal | Emphasize narration or a short key phrase | Preserve exact approved overlay text and adequate reading time |
| RMP-04 | Background gradient/mesh | Add restrained depth to a background | Keep contrast stable and avoid visual noise behind health information |
| RMP-05 | Colour-grade overlay | Harmonize mixed visual assets | Do not shift warning, brand or health-significant colours without approval |
| RMP-06 | Procedural grain/texture | Optional film-like texture | Omit when it reduces contrast, increases noise or harms accessibility |
| RMP-07 | Vignette/focus treatment | Direct attention toward the intended subject | Do not obscure text, logos, diagrams or clinically relevant details |
| RMP-08 | Ken Burns/pan-zoom on still | Add restrained movement to a static approved image | Optional only; preserve crop, visual facts and legibility |
| RMP-09 | Animated counter | Explain a sourced number or measured statistic | Number, unit, denominator, population, period and source remain S02/S01-locked; no fabricated count-up endpoints |
| RMP-10 | Radial mark/spark | Brand-approved accent or transition motif | Use only where brand/visual canon permits; never substitute decorative marks for meaningful symbols |
| RMP-11 | Scene/element exit | Clear an element or transition out of a beat | Keep exit timing inside the scene contract and avoid hiding required content |
| RMP-12 | Idle micro-motion | Subtle life in a non-critical decorative element | Never animate everything by default; static hold is a valid design decision |
| RMP-13 | Parallax depth | Create depth from approved layered assets | Requires layer separation, rights and continuity; do not invent unseen content |
| RMP-14 | Scene transition | Connect beats with cut, wipe, pan, scale or another supported transition | Choose by narrative relation and target support; cut is a valid and often safer default |
| RMP-15 | Motion blur | Reduce harshness of fast movement | Renderer support and visual QA required; omit when it obscures text or detail |
| RMP-16 | Audio-linked motion/SFX | Align a cue with an entrance, cut or beat | Timing precision must come from S09 evidence; estimated timing stays estimated |
| RMP-17 | Word/phrase-synchronized captions | Emphasize spoken content in subtitle/caption presentation | Requires actual transcript/timing evidence, readable holds, subtitle QA and non-audio comprehension |

## 3. Pattern selection contract

For every selected pattern, record at least:

- `pattern_id` and catalogue version;
- `project_id`, `scene_id`, `element_id` and `motion_spec_id`;
- intended narrative/learning function and the element it affects;
- source, approved message/claim and overlay references where relevant;
- S05 visual tokens/Guide locks and S06 shot/camera references;
- start frame, `end_frame_exclusive`, duration, fps, timebase, timing source, precision and rounding policy;
- coordinate system and units for position, scale, rotation, opacity, path and speed;
- easing intent and exact curve/spring parameters only when the selected target supports them;
- entry, action, anticipation, follow-through, settle, hold and exit phases as applicable;
- renderer target/version, feature evidence, unsupported properties and mapping-loss notes;
- accessibility/reduced-motion alternative, reading-time requirement, contrast and flicker notes;
- rights/provenance for all visual/audio assets;
- acceptance oracle, expected behavior, observed result and verification status.

If a field is not known, mark it `UNKNOWN`, `ESTIMATED`, `NOT_TESTED` or `NOT_APPLICABLE` with a reason. Do not fill missing values with invented precision.

## 4. Motion and interpolation integrity

1. Preserve the canonical half-open interval: `duration_frames = end_frame_exclusive - start_frame`.
2. Keep all keyframes and phases within the scene interval, ordered, unique and consistent with fps/timebase.
3. Declare easing explicitly for eased interpolation. Clamp extrapolation at the intended boundaries unless a documented overshoot is deliberate and tested.
4. Linear movement is not globally prohibited: use it only when a constant-rate trajectory is the deliberate design intent, label the rationale (for example `LINEAR_INTENT`), bound the interval and include an acceptance check. Do not let a library default silently introduce linear motion.
5. Spring parameters, cubic-bezier curves and motion-blur controls are renderer-specific. Do not assume that Remotion, a generative video model, GSAP and Lottie expose identical controls.
6. Avoid magic frame numbers. Convert from explicit seconds/timecode using the declared fps and rounding policy. Source-derived audio timing retains its original precision.
7. Holds, stillness, reduced motion and no-animation states are valid outputs. Motion density is chosen for comprehension, not to satisfy a universal movement quota.
8. Decorative grain, vignette, glow, hero-colour limits and multi-layer stacks are optional S05/S07 decisions, not universal acceptance requirements.

## 5. Visual tokens and continuity

- Use S05/Guide-03 as the owner of palette, typography, texture, lighting and visual language. A renderer `theme` object is an implementation of those tokens, not a competing canon.
- Preserve S13 MCG/Guide lock versions, immutable identity and approved controlled variations. Missing continuity state is not permission to invent a variation.
- Keep official names, numbers, health instructions, logos and claims as editable, source-linked overlays. Generated typography or visual embellishment must not mutate factual wording.
- Safe areas, aspect ratio, resolution and logo placement are project variables; static infographic margins do not define video composition.
- Choose background, grade, grain, vignette, glow and parallax only when they improve the declared narrative function and pass contrast/readability QA.

## 6. Audio and deterministic generation

- S09 retains source audio, transcript provenance, speaker identity, timing source/precision, music/SFX provenance and audio rights.
- Do not claim word-sync from a script estimate. Use `WORD_ALIGNED`, `PHRASE_ALIGNED`, `SEGMENT_ALIGNED`, `ESTIMATED` or another justified precision value from the actual source process.
- SFX may be synthesized only when requested/authorized and appropriate to the project. Silence is acceptable when audio is outside scope or no rights-cleared audio exists.
- When deterministic procedural audio or visuals are required, use a documented seed and stable pseudo-random procedure. Do not use unseeded randomness in render-time or release-critical generation. Record generator version and parameters.
- Music and SFX require source/licence/rights handling; an example source website is not a blanket licence grant.

## 7. Remotion capability and adapter boundary

Remotion is a concrete candidate target, not a global capability assertion. S10 must record the exact installed package versions, runtime, dependencies, browser, codecs, asset paths, fonts, permissions and inspection tools before selecting `PROGRAMMATIC` rendering.

The inspected Promkes Remotion V3 adapter profile is limited to:

- one selected/approved still reference per scene;
- editable React text overlays;
- sequential Remotion `Sequence` scenes;
- cut-only transitions;
- one centered scale-only motion record per scene, within its declared 1.0–1.15 range.

The current profile does not implement audio/sound cues, subtitle rendering, crossfades/non-cut transitions, arbitrary motion paths, multiple composited references, dynamic asset URLs or AI video-model generation. Unsupported records must fail closed or route to a separately verified adapter. Do not silently approximate or claim support for RMP patterns outside this profile.

Use the route states owned by S10: `NATIVE`, `PROGRAMMATIC`, `HANDOFF` or `NONE`. If Remotion packages, runtime or required capabilities are unavailable, provide a renderer-neutral handoff and keep render status `NOT_RUN`/`BLOCKED`; do not claim an MP4 exists.

## 8. Two-layer visual verification

Source-composition inspection and encoded-media inspection are distinct:

1. **Static/contract QA:** schema, semantic timing, IDs, source/claim refs, MCG dependencies, capability records and mapping-loss checks.
2. **Composition-frame QA:** inspect requested frame states from the actual composition/renderer. This checks composition behavior but not the final MP4 encoding.
3. **Encoded-media QA:** after an actual export, verify file existence/openability, codec, dimensions, fps, duration and streams where tools permit; extract frames from that MP4 and inspect them for crop, clipping, flicker, contrast, missing assets, text and continuity.
4. **Audio/subtitle QA:** only where actual audio/subtitle artifacts and inspection capability exist; check source correspondence, timing, clipping/loudness and sync using measurable or audible evidence.
5. **Human approval:** clinical, rights, brand, accessibility and release authorities remain separate from renderer QA.

A source `still` output cannot prove the encoded MP4 is correct. If encoded-media inspection cannot run, mark it `NOT_RUN` or `NOT_VERIFIED`. A test that only verifies a file exists is not visual QA.

## 9. Failure, fallback and reproducibility

- Missing runtime/dependency/browser/codec → `BLOCKED` or `HANDOFF`, with exact missing capability.
- Unsupported curve/path/transition/audio/subtitle → explicit mapping-loss entry and fail-closed route, not silent substitution.
- Render error → preserve prior approved output, capture logs, identify affected scene/element, retry only under a bounded policy and CHG-ID.
- Stale composition or output → re-render with explicit overwrite policy and verify the new artifact identity before inspection.
- Resource limit/disk shortage → stop safely and preserve source files.
- Unavailable visual inspection → `NOT_VERIFIED`; no claim of a clean pass.
- Any change to motion, renderer version, source asset, timing or QA oracle invalidates the relevant downstream evidence and requires targeted regression.

## 10. Acceptance checks

| ID | Observable acceptance condition |
|---|---|
| RMP-AC-001 | Every selected pattern has an ID, scene/element reference and declared narrative purpose |
| RMP-AC-002 | Every motion interval uses half-open frame semantics and reconciles with fps/timebase |
| RMP-AC-003 | Easing is explicit or a deliberate, bounded linear intent is documented |
| RMP-AC-004 | Unsupported renderer features are visible in a mapping-loss report or cause a fail-closed handoff |
| RMP-AC-005 | No pattern mutates S02-approved claims, factual overlays or MCG locks |
| RMP-AC-006 | Reduced-motion, reading-time, contrast and flicker concerns have a disposition |
| RMP-AC-007 | Audio sync and captions do not exceed actual S09 timing precision |
| RMP-AC-008 | Procedural release-critical output is reproducible from a recorded seed/configuration |
| RMP-AC-009 | Composition-frame QA and encoded-MP4 QA are separately reported |
| RMP-AC-010 | Any final render claim has a real artifact locator and corresponding inspection evidence |
| RMP-AC-011 | Asset provenance, rights/consent state and renderer capability are explicitly recorded |
| RMP-AC-012 | Defects, fallbacks, retries and invalidated dependencies are recorded and retested |

These are acceptance requirements for adoption, not claims that all checks have already run. The Remotion pattern library is `STATIC_SPECIFIED` until target integration and media tests are executed.
