# Architecture

## Topology

`M00 → S01–S13 → M00 integration → Prompt-to-Reference Production Package → downstream renderer (Remotion or equivalent)`

Skill files are modular instruction contracts, not independent agents unless the host truly executes them as such. M00 is the only final integrator.

## Domain ownership

| ID | Skill | Primary responsibility |
|---|---|---|
| S01 | source-asset-intelligence | Source/poster/caption extraction and provenance |
| S02 | health-evidence-safety-auditor | Health claims, evidence and fact locks |
| S03 | audience-campaign-strategy | Audience, behavior and campaign objective |
| S04 | story-screenplay-architect | Story, dialogue and VO script |
| S05 | visual-identity-art-direction | Visual canon, characters, environments and props |
| S06 | storyboard-cinematography | Storyboard, shots, viewpoint and composition |
| S07 | animation-motion-design | Renderer-neutral motion and timing references |
| S08 | ai-video-reference-engineering | Still/reference prompts and reference asset manifest; no text-to-video |
| S09 | voice-sound-design | Voice and sound reference cues |
| S10 | editing-postproduction | Renderer-neutral composition/scene/layer/timeline handoff |
| S11 | social-accessibility-distribution | Publishing copy and accessibility package |
| S12 | quality-assurance-controller | Independent reference package QA |
| S13 | continuity-guardian | MCG, seven Guide registry, locks and change control |

## Main dependency flow

`S01 → S02 → S03 → S04 → S05/S13 → S06 → S07 → S08 → S09 → S10 → S11 → S12 → M00`

Independent tasks may be combined when their inputs are ready. Domain ownership does not move. S13 integrates continuity locks across S04–S10. S12 routes defects back to the owning skill.

## Seven Guide modules

1. Master Character Guide.
2. Character Personality Guide.
3. Master Visual Style Guide.
4. Master Narrative Style Guide.
5. Master Voice & Audio Guide.
6. Master World & Environment Guide.
7. Scene Continuity Guide.

The MCG is an index and control record; it does not duplicate all Guide bodies.

## Output boundary

The plugin creates still/reference prompts, storyboard and motion reference data, audio/overlay references, an asset manifest, and a renderer-neutral composition handoff. It does not generate or render the final video, and it does not emit Remotion TSX by default. Downstream rendering has a separate implementation and QA lifecycle.
# Architecture V2 — Health-First Production System

## Topology

`M00 → S01–S13 → M00 integration → production manifest → (reference handoff | renderer adapter | verified media)`

Skill files are bounded instruction contracts. They are not proof of independent runtime agents or installed services. M00 is the sole project orchestrator and final integrator.

## Domain ownership

| ID | Skill | V2 responsibility |
|---|---|---|
| M00 | master-orchestrator | Input-mode routing, capability gates, state, integration, manifest and delivery aggregation |
| S01 | source-asset-intelligence | Poster/caption/script/source extraction and provenance |
| S02 | health-evidence-safety-auditor | Health claims, evidence, safe wording, fact locks; final domain authority stays human |
| S03 | audience-campaign-strategy | Audience, behavior objective, campaign message and CTA |
| S04 | story-screenplay-architect | Narrative, screenplay, dialogue and canonical VO wording |
| S05 | visual-identity-art-direction | Visual canon, characters, environment, props and design tokens |
| S06 | storyboard-cinematography | Scene, shot, camera, composition and scene timing mapped to source segments |
| S07 | animation-motion-design | Motion choreography, easing, timing, transitions and renderer constraints |
| S08 | ai-video-reference-engineering | Still/reference prompts, visual assets manifest and reference handoff |
| S09 | voice-sound-design | Audio intake/intelligence, transcript provenance, alignment status, voice direction, subtitle SRT/VTT and audio post plan/processing when tools exist |
| S10 | editing-postproduction | Composition, renderer adapter, project assembly, render/export and output-file verification when tools exist |
| S11 | social-accessibility-distribution | Social copy, platform packaging, accessibility, titles, alt text and hashtags |
| S12 | quality-assurance-controller | Independent content/reference QA plus conditional actual-media QA |
| S13 | continuity-guardian | MCG, seven Guide registry, canonical locks, scene state, versioning and change impact |

## Preserved authority hierarchy

1. System/platform and safety constraints.
2. Legal permissions, privacy, consent and institutional authority.
3. S02 Health Truth Registry and locked health wording.
4. S03 campaign objective and approved CTA.
5. S04 approved narrative and VO copy.
6. S05/S13 creative canon and continuity locks.
7. S06 scene/shot contract.
8. S07 motion specifications.
9. S09 verified audio/transcript/timing and audio deliverables.
10. S10 composition/render implementation details.
11. S12 independent QA disposition.

Downstream production cannot silently rewrite upstream truth. If a correction changes health meaning, return it to S02 and require authorized review.

## Input modes

- `POSTER_FIRST`: poster/caption first; S01 → S02 → S03 → S04 → visual/continuity → audio and render.
- `AUDIO_FIRST`: audio/transcript first; S09 intake → S02 claim verification → S03/S04 → visual/continuity → render.
- `HYBRID`: S01 and S09 intake independently; M00 reconciles source identity, transcript, captions and contradictions before downstream approval.
- `SCRIPT_FIRST`: text-only; audio metadata and exact timing are unavailable; timing remains `none` or `estimated`.

## Shared production state

The Promkes Production Manifest V2 is the single project-level source of truth for settings, provenance, health claims, campaign, narrative, audio, scenes, visual system, MCG refs, reference assets, motion, subtitles, sound cues, renderer, outputs, QA and delivery. Domain owners update only their fields. MCG remains the canonical index for the seven Guide modules; the production manifest references MCG/Guide IDs and does not duplicate their full bodies.

## Delivery classes

`BLUEPRINT_ONLY → REFERENCE_READY → RENDER_READY → RENDERED_PARTIALLY_VERIFIED → RENDERED_VERIFIED`

`BLOCKED` may occur at any stage. No status may be inferred from a polished text response. `RENDERED_VERIFIED` requires actual media and recorded checks; clinical/institutional approval and publication authorization are separate human-controlled states.

## Dependency graph

`Intake → (S01 source + S09 audio, when available) → S02 health truth → S03 campaign → S04 screenplay → S05 visual canon + S13 continuity → S06 storyboard → S07 motion → S08 reference prompts → S09 captions/audio post → S10 composition/render → S12 dual QA → M00 delivery`

S01 and S09 may intake concurrently only when independent inputs exist. Source facts and transcript uncertainties must be reconciled before factual story locks. Visual reference generation may proceed in parallel with audio preparation after the narrative/visual inputs are approved. Render requires the applicable assets, manifest validity, renderer capability, rights and permissions.

## Continuity and changes

MCG controls creative identity; the production manifest controls operational state. Every upstream change records changed IDs, affected downstream artifacts, invalidations and retests. Use targeted correction loops and preserve unaffected approvals.
