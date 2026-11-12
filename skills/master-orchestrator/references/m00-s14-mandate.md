# M00 mandatory S14 entrypoint — V4.1.3

For every conversation-history audit, plugin/version update, private/public source reconciliation, GitHub publication or release-readiness decision, M00 must apply `s14-integration-contract.md` before changing versioned artifacts.

The preflight must: (1) record accessible sources and coverage boundary; (2) classify EXPLICIT, CONFIRMED_PREFERENCE, INFERRED, PROPOSED, UNKNOWN and SUPERSEDED; (3) create/update a register conforming to `schemas/v4/conversation-context.schema.json`; (4) trace source/context → requirement → owner/artifact → change → dependencies → tests/evidence → release status; (5) map source-tree gaps, canonical naming ambiguity and unresolved ownership without pretending same-slug files are identical; (6) identify stale evidence and affected tests; (7) report private save/read-back, GitHub commit/PR/CI/review/merge, host, external AI, renderer, media QA, rights, license and human approval separately.

A context register is not clinical evidence, campaign-fact verification, permission, identity or test evidence. If raw history is inaccessible, disclose PARTIAL_WITH_DISCLOSED_BOUNDARY. If preflight cannot be produced, mark NOT_RUN; do not imply PASS. S14 is cross-cutting and does not replace S02 health authority, S12 independent QA or human approvals.
