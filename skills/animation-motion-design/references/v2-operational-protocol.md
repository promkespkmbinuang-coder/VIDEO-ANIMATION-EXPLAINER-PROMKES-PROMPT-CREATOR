# S07 V2 Operational Protocol — Animation & Motion Design

## Ownership and boundary
S07 owns motion choreography, element state transitions, motion paths, keyframes, transforms, easing, phase timing and reduced-motion alternatives. S06 owns shot/camera intent; S13 owns global character/scene continuity; S10 owns renderer mapping and execution.

## Procedure
1. Consume approved S06 scene/shot contract and S05/S13 visual identity locks.
2. Define each moving element with stable `element_id`, scene ID, start/end state, trigger, intended action and narrative purpose.
3. Specify phase structure: anticipation, action, follow-through, settle and hold where relevant.
4. Record keyframes in strictly increasing order using explicit `fps`, `timebase`, coordinate/scale/rotation units, easing function and parameter ranges.
5. Describe motion path, collision/occlusion, camera-relative/world-relative space, bounds and negative constraints.
6. Define entry and exit state; compare outgoing and incoming scene states with S13.
7. Declare reduced-motion/low-motion fallback and readability requirements.
8. Map to renderer-neutral records; renderer-specific unsupported controls become a technical change request to S10-RE, not silent substitution.

## Decision rules
- No unitless transforms or ambiguous timebase.
- Frame ranges use declared half-open arithmetic and cannot exceed scene bounds.
- Keyframes must be ordered, bounded and use supported easing identifiers.
- Character pose/position/prop state cannot contradict MCG or adjacent scene locks.
- Motion must support message comprehension, not obscure health overlays or CTA.

## Negative cases
Missing units/fps; descending or duplicate keyframes; unsupported easing; motion range outside scene; unbounded scale/position; inconsistent state-in/out; flashing/flicker; inaccessible text movement; and renderer target overclaim.

## Output contract
`Animation & Motion Specification`: element registry, state model, motion record, keyframes, path/transform, phase choreography, easing, timing provenance, continuity links, accessibility fallback, renderer-neutral constraints and acceptance checks.

## Acceptance
All motion records are measurable and interpretable, preserve scene continuity, and remain truthful about renderer feasibility.
