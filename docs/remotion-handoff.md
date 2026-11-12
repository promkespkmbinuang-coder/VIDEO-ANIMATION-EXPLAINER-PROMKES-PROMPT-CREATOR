# Remotion / renderer handoff (reference only)

This document describes how the output of this plugin can be interpreted by a downstream Remotion project. It is not a Remotion implementation or a guarantee that a generic manifest is directly executable.

## Concept mapping

| Plugin reference concept | Possible downstream Remotion concept |
|---|---|
| Project canvas | Composition width / height |
| Target frame rate | Composition fps |
| Total duration | Composition durationInFrames |
| Scene order and frame ranges | Sequence / Series.Sequence timing |
| Reference asset IDs | Resolved static/media asset paths |
| Layer role and z-order | React layer ordering |
| Transform / opacity / crop | Style or animated component props |
| Overlay/subtitle records | HTML/SVG/text overlay components |
| Audio cue IDs and ranges | Audio components and sequence timing |
| Renderer-neutral scene manifest | Candidate JSON-serializable inputProps, after schema adaptation |

## Required downstream implementation decisions

- Define the React component tree and registered composition IDs.
- Define and validate a concrete TypeScript/Zod schema for input props.
- Map every approved `reference_id` to an actual asset path or URL available to the renderer.
- Define frame-rate/timebase conversion and rounding policy.
- Implement transitions, animation curves, text rendering, subtitles and audio mixing.
- Resolve font licensing, asset licensing, image consent and media provenance.
- Define render environment, codec, output path, retries and artifact QA.

Remotion documentation explains that compositions define component, dimensions, frame rate, duration and ID, and that JSON-serializable input props can be supplied to the composition. The downstream project must implement its own schema and components.
