# Output-mode migration: 1.0.x → 1.1.0

The default deliverable has changed from a video-generator prompt package to a **Prompt-to-Reference Production Package**.

| Previous framing | 1.1.0 framing |
|---|---|
| Master Video Prompt | Master Visual Reference Prompt |
| Scene-by-scene video prompts | Scene keyframe / still-reference prompts |
| Video-generator animation instruction | Separate S07 motion/timing reference data |
| Prompt as if a generator renders moving scene | Reference prompts for still assets and visual states |
| Rendering settings as expected prompt behavior | Renderer-neutral composition/asset/timing handoff |
| Video generation output | Downstream Remotion or similar render step (out of scope by default) |

No source facts, health constraints, story ownership, seven Guide architecture, S01–S13 responsibilities, or human approval rules are relaxed by this change.

The plugin may support a separately requested renderer implementation later, but this is a separate scope with concrete project schema, assets, component/code requirements, environment, permissions and artifact acceptance tests.
