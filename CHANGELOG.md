# Changelog

## 2.0.0
- Extended intake to poster-first, audio-first, hybrid and script-first production modes.
- Expanded S09 into Audio Intelligence, Voice & Sound Production with transcript provenance, source comparison, speaker/segment IDs, timing granularity, uncertainty logging, SRT/VTT, cue sheets and voice-first audio post controls.
- Expanded S10 into Composition, Renderer Integration, Render & Export with capability discovery, adapter contracts, proof render, full export, file verification and bounded troubleshooting.
- Expanded S12 into dual-layer QA for reference/content integrity and actual rendered media, with explicit `NOT_RUN` / `NOT_VERIFIED` handling.
- Added Promkes Production Manifest V2 schema as the shared project state contract.
- Added conditional delivery states from blueprint to verified media; technical delivery remains separate from human clinical/institutional approval.
- Added explicit audio, timing, rendering, export, rights, synchronization and media-inspection acceptance cases.
- Preserved Health Truth Registry, campaign strategy, MCG/seven Guides, prompt-to-reference safety boundary and existing S01–S13 specialist ownership.

## 1.2.2
- Removed a fixed-version assumption from the validator; it now checks semantic-version syntax and manifest parity so patch/minor releases do not require validator edits solely to advance version.
- CI-discovered test-schema validation remains suite-aware: baseline AT and reference REF cases keep their distinct required fields.


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
## 1.2.1
- Corrected strict test-schema validation to respect the distinct AT and REF case contracts.

## 1.2.0
- Added strict YAML frontmatter parsing, reference validation, compatibility manifests and requirement/test/owner/dependency/output traceability.

## 1.1.0
- Clarified Prompt-to-Reference boundaries and downstream renderer handoff.

## 1.0.0
- Initial modular release M00 + S01–S13.
