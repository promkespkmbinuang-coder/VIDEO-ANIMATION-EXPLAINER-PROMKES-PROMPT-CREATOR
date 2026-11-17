# Promkes V2 Deterministic Enforcement CLI

This command-line surface executes deterministic repository checks. It does not invoke the ChatGPT host, an external AI provider, clinical authority, or a renderer unless such capabilities are separately configured and directly observed.

Run commands from the repository root with the development dependencies installed.

## Run tests

```bash
PYTHONPATH=. python -m scripts.promkes_v2 run-acceptance
PYTHONPATH=. python -m scripts.promkes_v2 run-acceptance --all-regression
PYTHONPATH=. python -m pytest -q tests/test_v2_acceptance.py tests/test_v2_hardening.py
```

## Scan actual untrusted source text

`scan-intake` consumes a JSON object with a non-empty `sources` array. Every source must contain readable text or be handled by an injected, trusted text extractor. Missing text or scanner errors return BLOCKED. A no-pattern-match result is not a proof that text is safe.

```bash
PYTHONPATH=. python -m scripts.promkes_v2 scan-intake intake.json
PYTHONPATH=. python -m scripts.promkes_v2 scan-boundary transformed-text.json
```

`scan-boundary` never grants tool authorization. A separate trusted workflow must decide whether an action is allowed; scanned source text never has authority to request or approve a tool call.

## Validate a handoff

The semantic handoff command requires all of the following:

- a handoff JSON file;
- an externally managed artifact-index JSON file located outside the audited project root;
- the externally pinned SHA-256 of that exact artifact-index file;
- the project root, constraining artifact byte paths;
- the expected producer ID taken from M00 dispatch context, not from the handoff itself;
- dependency-status JSON whenever a `DEPENDS_ON` trace exists.

```bash
PYTHONPATH=. python -m scripts.promkes_v2 validate-handoff handoff.json \
  --artifact-index /secure/registry/artifact-index.json \
  --artifact-index-sha256 sha256:<64-hex-digest> \
  --project-root ./project \
  --expected-producer S03 \
  --dependency-statuses /secure/registry/dependency-statuses.json
```

Every input/output artifact reference must resolve to an indexed artifact, the index must agree with the envelope owner and hashes, and the actual bytes must match. Paths that escape the project root are rejected. A structural-only JSON Schema PASS is not a semantic handoff PASS.

## Verify a source snapshot

```bash
PYTHONPATH=. python -m scripts.promkes_v2 verify-snapshot snapshot.bin \
  --expected-hash sha256:<64-hex-digest> \
  --source-uri https://source.example/document \
  --support-location 'page 2, paragraph 4' \
  --accessed-at 2026-11-17T10:00:00+08:00
```

This proves byte/hash consistency and required provenance fields only. It does not prove the source's authority or that a clinician accepts its interpretation.

## Check a resource profile

The project input file carries route, candidate profile, usage and required categories. It must not contain an authority allow-list. The CLI requires a root-signed trust registry stored outside the project and an externally pinned root public key. Each resource profile record in that registry binds a profile ID and route to the exact canonical profile SHA-256.

```bash
PYTHONPATH=. python -m scripts.promkes_v2 check-budget budget-input.json \
  --trust-registry /secure/registry/trust-registry.json \
  --pinned-root-key <base64-root-public-key> \
  --project-root ./project
```

Modified ceilings, wrong routes, absent trust records, invalid signatures, expired registries, missing declarations, NaN/Infinity, booleans and negative values fail closed. Organizational ceilings and the root-key provisioning process must be established by the responsible authority.

## Validate the canonical control registry

```bash
PYTHONPATH=. python -m scripts.promkes_v2 validate-control-registry \
  --registry schemas/v4/control-registry.v2.json
```

This checks Draft 2020-12 schema validity plus exact registry metadata parity against the executable V4 control inventory and explicit legacy aliases.

## Status interpretation

- `PASS`: the deterministic code path produced the expected result for the executed fixture/input.
- `PASS_WITH_ISOLATION`: source text had no heuristic hit and remains isolated as data; this is not a safety or tool-authorization decision.
- `QUARANTINE`: suspicious text was detected and must not be treated as instructions.
- `BLOCKED`: mandatory input, trust, provenance, budget or execution context is absent/invalid.
- `NOT_RUN` / `NOT_VERIFIED`: capability or required evidence was not actually observed.

Even a complete local test suite does not establish live host invocation, clinical correctness, institutional authority, rights clearance, actual render, MP4 inspection, accessibility approval or release authorization.
