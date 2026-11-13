# GUIDE-06 — Master World & Environment Guide

Sole primary owner: S05 visual-identity-art-direction. Status: template only; project instances start DRAFT.

## Ownership boundary
World rules, locations, spatial layout, recurring props, environmental relationships, background identity and physical continuity. Does not own screenplay, camera blocking or motion timing.

## Required instance fields
project_id, guide_id, guide_version, status, primary_owner, source_refs, canonical_decisions, assumptions, unknowns, dependencies, affected_scenes, approval_record_ids, change_history_ref and content_hash.

## Adaptive continuity
Classify location identity and world rules as IMMUTABLE where appropriate; environmental states as CONTROLLED_VARIATION only when approved; object state, weather/time and scene layout as SCENE_DEPENDENT when the story requires it.

## Approval and change
LOCKED requires a human approval bound to exact content hash, version and scope. Material changes use CHG-ID, affected scenes/assets/prompts, regression cases, rollback and reapproval status. Preserve superseded decisions.
