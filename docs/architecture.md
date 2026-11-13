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


## V4.1.7 additive motion and adapter layer

The existing S06/S07/S08/S10/S12/M00/S13 ownership model is retained. S06 owns camera and shot plans; S07 owns quantified element motion records; S08 owns prompt compilation and version-pinned model dialect adapters; S10 owns renderer field mapping; S12 owns independent cinematic QA; S13 owns continuity; M00 arbitrates dependencies and gates. No S15 is added.

Motion records are validated by schemas/v4/motion-record.schema.json and scripts/validate_motion_contract.py. Platform adapter evidence is represented by schemas/v4/video-platform-adapter.schema.json. These are additive contracts and do not assert that any target model or renderer has been tested.
