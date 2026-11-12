# Renderer Integration & Export Contract

## Purpose

Extend S10 from a renderer-neutral handoff owner into a capability-gated adapter, assembly, export and file-verification owner. This does not bundle a renderer or guarantee that Remotion, FFmpeg, browser rendering or another engine exists in the current host.

## Capability matrix

Check each operation independently and record evidence:

| Capability | Required evidence |
|---|---|
| Read project/assets | Successful file access and exact paths/IDs |
| Execute code | Authorized runtime and successful safe check |
| Renderer availability | Actual renderer identity/version and invocation route |
| Dependencies | Installed/available versions, no assumed network install |
| Fonts/media | Required fonts and media decoders available |
| Codec/export | Target container/video/audio codecs supported |
| Storage | Permitted output path or host attachment route |
| Media inspection | Actual metadata, frame and/or audio inspection capability |

Statuses: `VERIFIED`, `UNAVAILABLE`, `NOT_TESTED`, `NOT_APPLICABLE`.

## Route selection

1. **Native route:** a native video/motion artifact is available in this exact session and provides required audio sync/export.
2. **Programmatic route:** an actual accessible runtime and renderer (for example Remotion or FFmpeg) can assemble and export the project.
3. **Handoff route:** no supported renderer; deliver manifest, assets, timeline, subtitles, audio cues, adapter contract and build instructions. No MP4 is claimed.

A model that creates short video clips is not automatically a deterministic multi-scene timeline renderer.

## Assembly rules

- Manifest is the single source of truth for scene IDs, time ranges, asset IDs, captions, overlays, audio cues and render settings.
- Target schema must be validated against the exact renderer project. Generic JSON is not automatically valid Remotion props or TSX.
- Keep health copy, numbers, dates, CTA, logo and subtitles as separately editable overlay layers.
- Respect safe areas, alpha, font fallbacks, z-order, crop, frame/time mapping, transitions and audio synchronization.
- Missing critical assets, unlicensed audio, unresolved factual locks or incompatible timeline block publish-ready export.

## Render sequence

1. Validate manifest and referenced assets.
2. Validate scene/frame arithmetic, fonts, overlays and audio references.
3. Produce a short/low-resolution proof render if feasible.
4. Inspect proof render for layout, timing, A/V sync and missing assets.
5. Correct evidence-based defects; record changed IDs and invalidations.
6. Render the full output only after proof checks pass.
7. Verify file existence, openability, container, dimensions, fps, duration, video/audio streams and sync to the extent supported.
8. Capture actual error messages and classify failures; retry once only after a specific correction, not in an unbounded loop.

## Delivery states

`BLUEPRINT_ONLY`, `REFERENCE_READY`, `RENDER_READY`, `RENDERED_PARTIALLY_VERIFIED`, `RENDERED_VERIFIED`, `BLOCKED`.

`RENDERED_VERIFIED` requires the actual output plus evidence for all critical checks. Unsupported checks remain `NOT_VERIFIED`; they cannot silently pass. A render is not clinical approval or publication clearance.
