# S06 V2 Operational Protocol — Storyboard & Cinematography

## Ownership and boundary
S06 owns scene segmentation, shot list, cinematography, framing, camera intent, composition and timeline structure. S07 owns object/character motion mechanics. S13 owns cross-scene state continuity. S09 owns measured audio timing. S06 does not invent exact VO timing when no alignment evidence exists.

## Procedure
1. Require approved campaign/story/visual inputs and S02 factual locks.
2. Segment script/transcript into semantic beats; preserve source segment IDs and wording lineage.
3. For each scene/shot define purpose, message/claim refs, shot scale, viewpoint, framing, focal hierarchy, camera intent, subject placement, transition and scene in/out state.
4. Determine timing provenance: `MEASURED` from S09 alignment, `ESTIMATED` from explicitly declared method, `PROFILE` from approved duration profile, or `NONE`.
5. Never create a hidden default duration. Missing duration without an approved profile is `BLOCKED` for frame-accurate timeline acceptance.
6. Convert time to frame ranges only with declared fps, timebase, rounding rule and source precision.
7. Validate half-open `[start_frame, end_frame)` arithmetic, ordering, gaps and overlaps. Every overlap must match a declared transition.
8. Publish scene contracts for S07, S08, S10 and S13 with stable IDs.

## Decision rules
- Unknown duration remains unknown; a visibly labeled estimate may support planning but not exact synchronization.
- Audio-free SCRIPT_FIRST mode uses `NONE` or an explicit estimate, never word-level measured timing.
- A scene with unresolved health/visual lock remains held downstream.
- Camera intent is distinct from motion of characters/objects.

## Negative cases
Unmeasured exact word timing; missing fps; mixed timebases; negative or zero duration; overlapping scenes without transition declaration; silent gaps; missing source segment; unsupported camera move; and script changes that do not update scene references.

## Output contract
`Storyboard + Cinematography Shot List`: scene/shot IDs, beat purpose, claim/message refs, source segment, frame/time data, fps/timebase, camera/framing intent, transitions, safe areas, scene in/out states, dependencies and acceptance checks.

## Acceptance
A renderer can interpret the timeline deterministically without inventing duration, camera intent or synchronization precision.
