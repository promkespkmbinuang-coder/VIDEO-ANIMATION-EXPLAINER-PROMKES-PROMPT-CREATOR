# Requirements and acceptance traceability

## Traceability contract

Traceability is maintained as a machine-readable, one-to-one join in `tests/traceability.json`. Every test in `tests/acceptance-cases.json` and `tests/reference-output-cases.json` must have exactly one record with:

- `requirement_ids`: requirements directly exercised by the test;
- `owner_skill`: the canonical skill responsible for the behavior under test;
- `dependency_ids`: prerequisite test cases whose contracts/evidence are required;
- `output_ids`: output artifacts or control records whose acceptance is being checked.

This sidecar design keeps test fixtures/oracles readable while making the requirement–test–owner–dependency–output relationship queryable and validator-enforced. The validator fails on missing, duplicate, unknown, orphaned, or invalid references. A future schema migration may inline these fields into each test object, but the sidecar is the canonical traceability source for this release.

## Requirement registry

The canonical requirement catalog is in `tests/traceability.json` and includes the baseline `REQ-01`–`REQ-10`, non-functional `NFR-01`–`NFR-03`, and Prompt-to-Reference contract `REQ-REF-01`–`REQ-REF-09`.

| Requirement family | Scope | Main owners |
|---|---|---|
| REQ-01–REQ-10 | Source fidelity, health safety, campaign intent, narrative, continuity, storyboard/motion, reference prompt, text/accessibility, renderer handoff, QA/release | S01–S13 / M00 |
| NFR-01–NFR-03 | Portability, traceability/version control, reliability/recovery | M00 / S12 / S13 |
| REQ-REF-01–REQ-REF-09 | Reference-only boundary, Guide-linked references, keyframes, motion separation, exact overlay data, asset lifecycle, renderer-neutral handoff, Remotion boundary, artifact QA evidence | S02 / S05–S12 / M00 |

## Coverage and status

- `AT-001`–`AT-045`: baseline acceptance specifications.
- `REF-001`–`REF-013`: Prompt-to-Reference contract specifications.
- All 58 cases must be represented in `tests/traceability.json`.
- All acceptance case statuses remain `NOT_RUN` until the specific oracle has been executed and evidence recorded.
- Static package validation is not an acceptance-test pass and does not establish runtime compatibility, clinical correctness, renderer correctness, or video quality.

## Change impact procedure

1. Identify the changed requirement ID(s).
2. Query `tests/traceability.json` for every case whose `requirement_ids` include those IDs.
3. Include dependency descendants and any case whose `output_ids` overlap the changed contract.
4. Identify `owner_skill` and route repair to that domain owner; M00 integrates but does not overwrite specialist-owned content.
5. Re-run relevant static checks and execute affected dynamic cases on the named host/model/renderer.
6. Record actual input fixture, host/model/version, timestamp, output/evidence locator, oracle result, reviewer, and residual limitation.

## No inferred pass

A documented test, a successful export, a valid manifest, or an empty CI result is not evidence that a model/host generated correct output. A status may become `PASS` only when its oracle and evidence are recorded. Otherwise use `NOT_RUN`, `BLOCKED`, or `NOT_APPLICABLE` with a reason.
