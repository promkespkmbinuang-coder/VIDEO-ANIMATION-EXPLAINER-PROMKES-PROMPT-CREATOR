# GUIDE-07 — Scene Continuity Guide

**Sole primary owner:** S13 `continuity-guardian`. Status: template only; instances start DRAFT.

## Ownership boundary
Integrated scene-in/out state, Guide and lock references, versions, dependency indexes and cross-scene continuity. S13 integrates but does not author GUIDE-01 through GUIDE-06 or take over their domain records.

## Required fields
`project_id`, `guide_id`, `guide_version`, `status`, `primary_owner`, `scene_refs`, `continuity_in`, `continuity_out`, `guide_version_refs`, `lock_refs`, `dependencies`, `affected_assets`, `approval_record_ids` and `change_history_ref`.

## Mandatory refresh
After storyboard and contributing S07 motion, S09 audio/time and S10 edit context are available, S13 refreshes affected scene states and MCG version. S08 compilation is blocked until this refresh is validated.

## Adaptive continuity and approvals
Track IMMUTABLE, CONTROLLED_VARIATION and SCENE_DEPENDENT attributes separately. LOCKED requires human approval bound to exact hash, version and scope. Preserve old states and change references; never silently rewrite history.
