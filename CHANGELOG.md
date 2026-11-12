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
- Corrected strict test-schema validation to respect the distinct AT and REF case contracts.

## 1.2.0
- Added strict YAML frontmatter parsing, reference validation, compatibility manifests and requirement/test/owner/dependency/output traceability.

## 1.1.0
- Clarified Prompt-to-Reference boundaries and downstream renderer handoff.

## 1.0.0
- Initial modular release M00 + S01–S13.
