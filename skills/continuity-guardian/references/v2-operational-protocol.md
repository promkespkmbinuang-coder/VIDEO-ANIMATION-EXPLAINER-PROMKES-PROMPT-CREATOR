# S13 V2 Operational Protocol — Continuity Guardian

## Ownership and boundary
S13 owns MCG as canonical index, seven-Guide registry, Global Continuity Locks, Scene Continuity Ledger, versioning and change-impact/invalidation governance. Domain specialists author the contents of their Guides; S13 does not replace S04/S05/S06/S07/S09/S10 domain ownership.

## Canonical seven-Guide ownership

| Guide | Canonical owner | Contributor boundary |
|---|---|---|
| GUIDE-01 Master Character Guide | S05 | S04 may provide personality/story traits |
| GUIDE-02 Character/Profile & Personality | S04 | S05 contributes visual appearance |
| GUIDE-03 Master Visual Style Guide | S05 | Brand owner confirms official rules |
| GUIDE-04 Master Narrative Style Guide | S04 | S03 supplies campaign intent |
| GUIDE-05 Master Voice & Audio Guide | S09 | S04 supplies approved VO text |
| GUIDE-06 Master World & Environment Guide | S05 | S06 supplies shot/location requirements |
| GUIDE-07 Scene Continuity Guide | S13 | S06/S07/S09/S10 contribute scene state and timing |

## Procedure
1. Select MCG-Lite/Standard/Advanced depth based on project complexity and risk.
2. Register exactly one stable Guide ID, version, status and owner for each applicable Guide type.
3. Preserve authoring authority: S13 indexes and locks; the named owner authors detailed content.
4. Create scene continuity ledger with state-in/state-out, character/prop/environment identity, Guide versions and dependency references.
5. Lock only accepted content; maintain previous versions and source trace.
6. On a change, compute dependency closure from the canonical graph, validate DAG and identify only affected downstream artifacts.
7. Invalidate affected approvals and derivatives; preserve unaffected branches.
8. Require retest/reapproval of affected artifacts before re-locking.

## Decision rules
- Duplicate Guide ID, multiple conflicting owners for one Guide record, unknown Guide type or owner mismatch → `FAIL`.
- Scene referencing stale/unlocked Guide version → `HOLD` and invalidate affected dependent artifacts.
- Dependency cycle → `BLOCKED`; do not guess an invalidation order.
- `expected_invalidated` embedded in the project is not an oracle. Compute closure independently from graph specification.
- Invalidation records must preserve prior snapshot, changed IDs, affected refs, old/new hashes, retests and rollback reference.

## Negative cases
Undocumented retcon; stale lock; missing Guide; duplicate Guide owner; cycle in dependency graph; Guide change that fails to invalidate its downstream scene/reference/render; and overbroad invalidation of unrelated audio or campaign branches.

## Output contract
`MCG + Guide Registry + Scene Continuity Ledger + Global Locks + Change Impact Report`: include canonical owner, Guide version/status, scene state refs, dependency closure, invalidation event, retained unaffected artifacts, retests and acceptance evidence.

## Acceptance
A reviewer can trace every scene to one current Guide version and explain exactly which artifacts were invalidated by any upstream change—and why unrelated branches remain intact.
