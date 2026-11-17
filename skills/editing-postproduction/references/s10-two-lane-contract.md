# S10 V2 Two-Lane Operational Contract

## Public identity
S10 remains `editing-postproduction`; no public skill ID, name, path or trigger is replaced. `S10-MP` and `S10-RE` are internal lane IDs only. They are not separate plugins or claims of independent agents.

## Lane ownership

| Responsibility | S10-MP — Media Production | S10-RE — Renderer Engineering |
|---|---|---|
| Editorial order, pacing, transitions | DECIDE | IMPLEMENT |
| Composition, layer hierarchy, crop/safe areas | DECIDE | MAP TO RENDERER |
| Timeline and scene assembly | AUTHOR | VALIDATE/IMPLEMENT |
| Overlay/subtitle/audio placement | AUTHOR EDITORIAL PLACEMENT | IMPLEMENT |
| Target renderer capability/version | CONSUME | VERIFY |
| Adapter/code/typed props | NO | AUTHOR |
| Build/integration/runtime | NO | EXECUTE/REPORT |
| Render/export | MAY REQUEST | EXECUTE ONLY WHEN VERIFIED |
| Actual media verification | PROVIDE REQUIREMENTS | CAPTURE TECHNICAL EVIDENCE; S12 INDEPENDENTLY QA |

## S10-MP input/output
Inputs: locked MCG/Guide refs, approved scenes/shots/motion, asset manifest, audio/subtitle package, S11 accessibility constraints and render brief. Output: `MEDIA-PRODUCTION-HANDOFF` containing `composition_id`, editorial decision list ref, scene order, shot map, layers with stable IDs/z-order/source refs, overlay map and claim refs, subtitle map, audio map, safe areas, fps/timebase, resolution, duration basis, transitions and export profile.

## S10-RE input/output
Inputs: validated Media Production Handoff and verified capability/permission evidence. Output: `RENDERER-ENGINEERING-REPORT` containing exact runtime/provider/version, adapter mapping, source/build status, dependency/font/codec checks, proof render status, render log, actual output ref/hash, media metadata inspection and residual limitations.

## Boundary rules
1. S10-RE cannot silently change editorial meaning, claim wording, approved scene order or visual canon.
2. Incompatibility produces `TECHNICAL_CHANGE_REQUEST` with unsupported feature, consequence and alternatives. S10-MP decides editorial changes; M00 arbitrates cross-domain impact.
3. Rendering requires capability `VERIFIED`, exact version, explicit permission, approved resource profile and rights-ready inputs.
4. Runtime unavailable → `HANDOFF`/`UNAVAILABLE`; no render claim. Build PASS with no file → `RENDER_READY`, not rendered. Existing file without inspection → `NOT_RUN`/`NOT_VERIFIED`.
5. Only S12 can issue independent actual-media QA. Technical S10 checks cannot self-approve release.

## Acceptance
Both lanes validate against the shared handoff envelope, S10 lane-specific composition contract and universal artifact references. Every implementation change preserves the upstream composition hash or records an approved editorial change and its dependency invalidation.
