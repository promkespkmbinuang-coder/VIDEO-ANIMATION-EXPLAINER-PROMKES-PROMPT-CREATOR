# MCG and Guide module templates

## Master Continuity Guide (MCG)

| Field | Value |
|---|---|
| Project ID | `[PRJ-ID]` |
| Project title | `[TITLE]` |
| Campaign/topic | `[TOPIC]` |
| MCG version | `[VERSION]` |
| Complexity mode | `LITE / STANDARD / ADVANCED` |
| Status | `DRAFT / READY_FOR_STORYBOARD / READY_FOR_SCENE_PROMPTS / READY_FOR_HANDOFF / READY_WITH_LIMITATIONS / HOLD / BLOCKED` |
| Project owner | `[ROLE/UNKNOWN]` |
| Source dossier | `[SRC-REFS]` |
| Health Truth Registry | `[REGISTRY-REF/VERSION]` |
| Scene list | `[SCN-REFS]` |
| Change history | `[CHG-REFS]` |

## Guide registry

| Guide ID | Module | Owner skill | Version | Status | Dependencies | Affected scenes | Notes |
|---|---|---|---|---|---|---|---|
| GUIDE-01 | Master Character Guide | S05 | 1.0 | DRAFT | Source/story | `[SCENES]` | Detailed spec authored by S05 |
| GUIDE-02 | Character Profile / Personality Profile | S04/S05 | 1.0 | DRAFT | Story/character | `[SCENES]` | Split narrative and visual ownership explicitly |
| GUIDE-03 | Master Visual Style Guide | S05 | 1.0 | DRAFT | Brand/art | `[SCENES]` | |
| GUIDE-04 | Master Narrative Style Guide | S04 | 1.0 | DRAFT | Campaign/script | `[SCENES]` | |
| GUIDE-05 | Master Voice & Audio Guide | S09 | 1.0 | DRAFT | Script/audio | `[SCENES]` | |
| GUIDE-06 | Master World & Environment Guide | S05 | 1.0 | DRAFT | Art/locations | `[SCENES]` | |
| GUIDE-07 | Scene Continuity Guide | S13 integrates; S06/S07/S09/S10 contribute | 1.0 | DRAFT | Scene/audio/edit | `[SCENES]` | S13 governs the registry, owners author data |

## Guide instance record

`project_id`, `guide_id`, `guide_name`, `guide_version`, `status`, `primary_owner`, `source_refs`, `canonical_decisions`, `assumptions`, `unknowns`, `dependencies`, `affected_scenes`, `last_changed_by_role`, `change_ref`.

Use statuses `DRAFT`, `PROPOSED`, `REVIEWED`, `LOCKED`, `REVISED`, `PARTIAL`, `NOT_APPLICABLE`, `BLOCKED`.

## Canonical Lock record

| Field | Value |
|---|---|
| Lock ID | `[LOCK-ID]` |
| Item/asset ID | `[ITEM-ID]` |
| Canonical definition | `[EXACT ACCEPTED STATE]` |
| Owner | `[S-SKILL]` |
| Basis | `[SOURCE/CREATIVE DECISION REF]` |
| Version | `[VERSION]` |
| Status/approval | `[PROPOSED/LOCKED + AUTHORITY]` |
| Scope | `[PROJECT/EPISODE/SCENES]` |
| Allowed variations | `[LIST]` |
| Prohibited variations | `[LIST]` |
| Dependents | `[SCENE/ASSET IDs]` |

## Scene Continuity Ledger

| Scene | Character state | Wardrobe/props | Environment/time | Emotion/action | Audio state | Continuity-in | Continuity-out | Lock versions |
|---|---|---|---|---|---|---|---|---|

## Change record

`CHG-ID | item | old version | new version | class | reason | authority/approval | affected scenes/dependents | regression cases | rollback | status`.
