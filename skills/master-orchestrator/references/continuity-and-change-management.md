# Continuity & Change Management

## MCG record

The Master Continuity Guide (MCG) is the one project-level index/control record for seven separate Guide modules. It stores project identity, registry, canonical decision links, lock IDs/versions, dependency references, open issues, change history and release state. It must not duplicate detailed module contents.

## Guide registry fields

`guide_id`, `guide_name`, `guide_version`, `status`, `primary_owner`, `source_refs`, `canonical_decisions`, `assumptions`, `unknowns`, `dependencies`, `affected_scenes`, `last_changed_by_role`, `change_ref`.

Allowed module states: `DRAFT`, `PROPOSED`, `REVIEWED`, `LOCKED`, `REVISED`, `PARTIAL`, `NOT_APPLICABLE`, `BLOCKED`.

## Canonical lock

Every lock identifies what is fixed, owner skill, approving role/authority if known, source/creative basis, version, effective scope, allowed variations, prohibited variations and affected scenes. Do not call an unapproved proposal a lock.

## Scene state ledger

Track scene-in/out states for recurring characters, props, location, time, orientation, emotion, wardrobe, body position, object state, lighting and audio state as relevant. Link each row to the scene contract and current lock version.

## Change record

`CHG-ID | item ID | previous version | new version | class | reason | decision/approval | affected skills/scenes/assets | tests to rerun | rollback/fallback | status`.

Change classes: `COSMETIC`, `PLANNED`, `STRUCTURAL`, `RETCON`, `CORRECTION`. Every non-cosmetic change requires impact analysis. Do not silently overwrite a past accepted decision.

## Dependency impact

When a canonical claim, character feature, voice profile, style rule, prop, location or scene changes:
1. Find direct dependents.
2. Traverse downstream dependencies.
3. Identify exact affected prompts, references, assets and scenes.
4. Re-run only affected acceptance/regression cases plus global critical checks.
5. Mark untouched dependent scope as not impacted only with a reason.
6. Update the MCG registry and release manifest after the change is accepted.

## Global Continuity Lock usage

Every scene prompt receives only applicable IDs, versions, reference assets, character state, allowed variations and continuity-in/out. If the model cannot preserve identity from textual prompts alone, disclose that generation consistency cannot be guaranteed and recommend supported reference assets or manual review.

## Regression triggers

Guide revision, prompt compiler change, model/provider version change, identity lock change, scene state change, editing overlay change, health fact change, asset replacement, and a previously observed continuity defect.
