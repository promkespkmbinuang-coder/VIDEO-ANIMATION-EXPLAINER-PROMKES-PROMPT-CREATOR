# Release and integrity model

## Output states

- `DRAFT`: reference package being composed.
- `STATIC_REVIEWED`: written references and schemas reviewed.
- `READY_FOR_REFERENCE_HANDOFF`: reference package meets documented criteria.
- `READY_WITH_LIMITATIONS`: usable with disclosed noncritical gaps.
- `HOLD` / `BLOCKED`: critical issue or prerequisite missing.
- `TESTED_ON_TARGET`: only after actual execution on a named image/reference model or host with recorded conditions.

## Reference asset states

`PROMPT_DRAFT`, `PROMPT_REVIEWED`, `REFERENCE_GENERATION_PENDING`, `REFERENCE_CREATED`, `REFERENCE_SELECTED`, `REFERENCE_APPROVED`, `MISSING`.

Do not claim generated/selected/approved unless the corresponding asset and review evidence exists.

## Downstream renderer states

`NOT_STARTED`, `IMPLEMENTATION_PENDING`, `RENDERED_UNREVIEWED`, `ARTIFACT_QA_PENDING`, `ARTIFACT_QA_PASSED`, `ARTIFACT_QA_FAILED`, `APPROVED_BY_AUTHORITY`, `PUBLISHED`.

These are separate from the plugin's reference handoff states. The plugin must not advance them without actual downstream evidence.

## Integrity chain

`INPUT → SOURCE FACT → HEALTH MESSAGE → OBJECTIVE → STORY → SCENE → REFERENCE PROMPT → REFERENCE ASSET → RENDER HANDOFF → DOWNSTREAM RENDER → ARTIFACT QA → HUMAN APPROVAL`.

Every important fact and asset should have traceable IDs, source/provenance, version and status. Missing evidence remains visible. No claim is upgraded by creative repetition.

## Renderer neutrality

A scene/reference manifest is structured reference data. It is not automatically a valid Remotion `inputProps` object or renderer project. The downstream implementation must validate the exact schema, map IDs to available assets, define React components/compositions, load fonts/media and establish a rendering environment.
