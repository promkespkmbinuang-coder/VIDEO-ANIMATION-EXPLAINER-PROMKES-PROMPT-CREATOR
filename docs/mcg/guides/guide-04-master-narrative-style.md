# GUIDE-04 — Master Narrative Style Guide

Sole primary owner: S04 story-screenplay-architect. Status: template only; project instances start DRAFT.

## Ownership boundary
Narrative voice, tone, pacing, dialogue, storytelling conventions and spoken-language style. Does not own medical truth, source verification or visual identity.

## Required instance fields
project_id, guide_id, guide_version, status, primary_owner, source_refs, canonical_decisions, assumptions, unknowns, dependencies, affected_scenes, approval_record_ids, change_history_ref and content_hash.

## Adaptive continuity
Classify attributes as IMMUTABLE, CONTROLLED_VARIATION or SCENE_DEPENDENT. Controlled variations must be explicit; scene-dependent wording/voice states cite scene IDs. Never intensify health claims for rhetorical effect.

## Approval and change
LOCKED requires a human approval bound to exact content hash, version and scope. Material changes use CHG-ID, old/new version, decision owner, affected scenes/assets/prompts, regression cases, rollback and reapproval status. Preserve superseded decisions.
