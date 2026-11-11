# Changelog

## 1.2.1
- Corrected strict test-schema validation to respect the distinct AT and REF case contracts; REF cases are not required to contain baseline-only `family` or `input_fixture` fields.
- Kept each of the 58 test specifications at `NOT_RUN`; this is a validator-schema correction, not an acceptance-test pass.


## 1.2.0
- Added strict YAML frontmatter parsing with duplicate-key rejection.
- Added checks for skill frontmatter/directory naming parity and the compatibility manifest.
- Added repository-wide local Markdown/supporting-reference and heading-anchor validation.
- Added an external URL workflow using lychee.
- Added machine-readable requirement–test–owner–dependency–output traceability for all 45 baseline and 13 Prompt-to-Reference test IDs.
- Updated GitHub publication guidance to the actual repository and review-branch workflow.
- Updated Cursor's official Agent Skills URL and synchronized publisher metadata.
- Documented unresolved license, runtime, external model, renderer and artifact QA gates without claiming them as passes.

## 1.1.0
- Clarified the default output contract as Prompt-to-Reference, not Prompt-to-Video.
- Replaced direct video-generation scene prompts with still/reference asset prompts.
- Added a renderer-neutral reference asset manifest and scene/composition handoff.
- Separated image reference prompts, motion/timing references, exact overlay/subtitle data and downstream rendering.
- Clarified that Remotion or similar rendering, renderer code and final video export are outside the default deliverable.
- Added 13 prompt-to-reference acceptance case specifications.

## 1.0.1 — 2026-11-11
- Packaging cleanup: excluded Python bytecode/cache artifacts from the plugin release.

## 1.0.0 — 2026-11-11
- Initial modular release: M00 plus S01–S13.
- Added health-truth locking, evidence status, canonical continuity Guide registry, scene-level prompt contracts, and release QA.
- Added acceptance-case specification, static package validator, cross-platform export helper, and GitHub Actions validation workflow.
- Dynamic tests against external AI model runtimes are specified but not claimed as executed.
