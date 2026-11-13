# GCL-01 — Global Continuity Lock

Apply only approved and relevant Guide/lock references to each scene. A lock is a scope-bounded invariant, not a generic instruction to keep it consistent.

Every lock records lock_id, attribute_id, Guide ID, single owner, canonical definition/reference, source or decision basis, version, scope, class, allowed/prohibited variations, dependent scenes/assets, approval record, hash and change reference.

S04 consumes S02 Fact Lock and GUIDE-02/04; S05 owns GUIDE-01/03/06; S06 references locks in shots; S07 owns temporal motion/state changes; S09 owns audio/voice; S10 consumes approved renderer inputs; S13 indexes locks and GUIDE-07 only; S08 receives validated still states, never temporal motion instructions.

Conflicts, missing refs or unapproved locks place affected scope on HOLD. Unknown provider features are omitted or marked NOT_TESTED.
