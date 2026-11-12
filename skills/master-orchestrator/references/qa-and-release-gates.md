# QA and release gates — Prompt-to-Reference

## Separate acceptance levels

1. **Reference package QA:** validates source traceability, Health Truth Registry, story/VO, prompt-to-reference type, IDs, Guide locks, reference manifest, storyboard/motion references and renderer-neutral handoff.
2. **Reference asset QA:** requires actual generated still/reference files and inspection evidence.
3. **Renderer integration QA:** requires a concrete downstream renderer project and validated input schema.
4. **Rendered artifact QA:** requires the actual video/audio/subtitle/project output and frame/time inspection.
5. **Human approval:** clinical/institutional and publication approval belongs to authorized humans.

A PASS at one layer never implies PASS at a later layer. If no generated reference or rendered asset is supplied, mark its QA `NOT_RUN` or `BLOCKED`.

## Ready for reference handoff

- All critical facts are locked or explicitly held.
- Reference prompts request stills/reference assets only.
- Asset prompts include IDs and applicable Guide/lock versions.
- Motion references are separate and linked to scenes.
- Exact facts/logos/CTA are separate overlay records.
- Renderer-neutral scene/asset/timing/layer/audio mapping is coherent.
- Open items and missing assets are visible.
