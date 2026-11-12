# Promkes Production Manifest V2

The manifest is the operational single source of truth. It is a machine-readable contract, not a database, runtime, or automatic persistence service. If no persistent store exists, keep it in the project artifact and state that limitation.

## Ownership

- M00: project identity, global state, conflict arbitration, delivery aggregation.
- S01: source dossier and source assets.
- S02: health claims, evidence, safe wording and locks.
- S03: campaign and behavioral objectives.
- S04: narrative and screenplay.
- S05: visual system and visual assets descriptions.
- S06: scenes, shots and camera data.
- S07: motion specifications.
- S08: reference prompts and reference asset lifecycle.
- S09: audio, transcript, timing, subtitles, sound design and audio post state.
- S10: renderer settings, adapter, render artifacts and export verification.
- S11: distribution/accessibility packaging.
- S12: independent QA records and defects.
- S13: MCG and Guide/lock references.

A specialist updates only its owned subtree. Downstream interpretation cannot overwrite source evidence.

## Mandatory invariants

1. Stable IDs for project, sources, claims, evidence, audio segments, speakers, scenes, assets, subtitle cues, sound cues, renders and defects.
2. Every health claim referenced by screenplay, overlay, subtitle or visual scene links to Health Truth Registry IDs.
3. Every audio-derived timestamp carries source and granularity.
4. Every scene references its source segment IDs where narration is present.
5. Every asset has source/provenance, rights status and lifecycle state.
6. Every scene uses compatible MCG/Guide lock versions.
7. Every render record links to manifest version, renderer route, settings and actual file evidence.
8. Every QA PASS links to observed evidence; absent media means artifact QA `NOT_RUN`.
9. Technical delivery and human approval remain separate.
10. Changes create a `CHG-ID` and an invalidation list; they do not silently rewrite approved history.

See `../skills/master-orchestrator/references/promkes-production-manifest.schema.json` for the JSON Schema contract.
