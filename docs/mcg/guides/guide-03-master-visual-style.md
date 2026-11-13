# GUIDE-03 — Master Visual Style Guide

Sole primary owner: S05 visual-identity-art-direction. Status: template only; project instances start DRAFT.

## Ownership boundary
Visual grammar, palette, medium, texture, lighting, typography and brand-safe visual treatment. Does not own story wording, clinical facts or temporal motion timing.

## Required instance fields
project_id, guide_id, guide_version, status, primary_owner, source_refs, canonical_decisions, assumptions, unknowns, dependencies, affected_scenes, approval_record_ids, change_history_ref and content_hash.

## Adaptive continuity
Classify attributes as IMMUTABLE, CONTROLLED_VARIATION or SCENE_DEPENDENT. Immutable values have no variations; controlled variations list approved options; scene-dependent values cite scene IDs and visual state.

## Approval and change
LOCKED requires a human approval bound to exact content hash, version and scope. Material changes use CHG-ID, old/new version, decision owner, affected scenes/assets/prompts, regression cases, rollback and reapproval status. Preserve superseded decisions.
