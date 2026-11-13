# CCM-01 — Continuity Change Management

Every material change gets CHG-ID, item ID, previous/new version, class, reason, source/intent, decision owner, approval ref, affected Guide/scene/asset/prompt/overlay/subtitle/render/QA refs, dependency closure, regression cases, rollback, status and timestamp.

1. Identify the authoritative owner record.
2. Traverse dependencies and reject broken refs, duplicate nodes, self-edges, cycles or deadlocks.
3. Mark affected dependents STALE/INVALIDATED; record unaffected scope.
4. Rebuild in dependency order and rerun impacted tests plus critical invariants.
5. Reapprove artifacts whose hash, content or scope changes.
6. Update MCG, Guide refs, scene contracts, asset registry and release manifest after acceptance.

S02 claim changes invalidate linked factual dependents only; S04 narrative changes affect GUIDE-02/04 and timing; S05 visual changes affect GUIDE-01/03/06; S07 motion changes affect scene/sync/renderer; S09 audio changes affect GUIDE-05/subtitles/sync; S10 renderer changes require adapter/render/media QA. No silent retcon. Missing authority or evidence means PENDING_HUMAN or BLOCKED.
