# Acceptance test specification — Prompt-to-Reference

Run the base production suite in `tests/acceptance-cases.json` together with the reference-output contract suite in `tests/reference-output-cases.json`.

Additional mandatory reference-output checks:
- no direct text-to-video prompts;
- each S08 prompt describes one still/reference asset;
- character/style/environment/prop references use stable IDs and Guide/lock versions;
- motion and timing are stored separately from image prompts;
- exact factual text remains editable overlay data;
- prompt, generated reference, selected reference and approved reference have separate states;
- renderer-neutral scene handoff maps scene IDs to references, timing, layers, overlays and audio cues;
- a generic handoff is not presented as executable Remotion inputProps or code;
- no rendering or artifact QA pass is claimed without actual downstream output.

All test specifications begin as `NOT_RUN`. A test may become PASS only with recorded observed evidence and the target environment.
