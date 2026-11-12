# Platform compatibility — reference generation vs rendering

## Two different capability layers

1. **Reference generation:** a model/tool creates still images or other source assets from S08 prompt-to-reference records. Capability support depends on each image/reference model and must be checked for aspect ratio, reference images, identity consistency, transparency, image editing and output format.
2. **Downstream composition/rendering:** a separate project assembles selected reference assets, motion/timing data, typography, subtitles and audio into a video. Remotion is one example; it uses React compositions and accepts configured metadata/input props. This plugin does not run that renderer by default.

## Contract by platform layer

| Layer | What this plugin supplies | What must be separately verified |
|---|---|---|
| AI host skills | Portable `SKILL.md` source | Discovery, invocation, relative reference loading and runtime behavior |
| Image/reference model | Still/reference prompt records | Reference-image input, edit controls, aspect ratio, output/resolution and identity consistency |
| Renderer | Renderer-neutral scene/asset/timing handoff | Target project schema, assets, components, fonts, transitions, audio, render environment and codec |

## Remotion mapping

Remotion supports compositions with dimensions, fps, duration and a React component. It also accepts JSON-serializable input props. The plugin's manifest is a reference contract only; downstream code must adapt it to the specific composition's schema and register the components that consume the data.

Official references:
- https://www.remotion.dev/docs/composition
- https://www.remotion.dev/docs/passing-props
- https://www.remotion.dev/docs/parameterized-rendering
- https://www.remotion.dev/docs/render

## Portability rule

Do not equate a platform skill folder with successful host execution, image generation, or video rendering. Keep these test classes separate: package/static, skill discovery, reference-model runtime, renderer-schema integration, renderer execution and artifact QA.
