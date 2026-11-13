# GUIDE-02 — Character Personality & Narrative Profile

Sole primary owner: S04 story-screenplay-architect. Status: template only; project instances start DRAFT.

## Ownership boundary
Personality, motivation, behavior, relationships and emotional/narrative arc. Does not own visual character design or clinical truth.

## Required instance fields
project_id, guide_id, guide_version, status, primary_owner, source_refs, canonical_decisions, assumptions, unknowns, dependencies, affected_scenes, approval_record_ids, change_history_ref and content_hash.

## Adaptive continuity
Classify attributes as IMMUTABLE, CONTROLLED_VARIATION or SCENE_DEPENDENT. Immutable values have no variations. Controlled variations enumerate approved options. Scene-dependent values cite scene IDs and continuity-in/out state.

## Approval and change
LOCKED requires a human approval bound to exact content hash, version and scope. Material changes use CHG-ID, old/new version, decision owner, affected scenes/assets/prompts, regression cases, rollback and reapproval status. Preserve superseded decisions.
