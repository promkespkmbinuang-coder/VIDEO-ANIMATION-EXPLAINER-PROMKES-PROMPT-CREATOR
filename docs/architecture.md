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
