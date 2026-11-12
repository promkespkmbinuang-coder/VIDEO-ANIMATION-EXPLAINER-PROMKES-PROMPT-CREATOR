# M00 mandatory S14 entrypoint — V4.1.2

M00 must load and apply `s14-integration-contract.md` when a request includes a conversation-history audit, plugin/version update, private/public source reconciliation, GitHub publication or release-readiness decision.

The preflight must create a context register conforming to `schemas/v4/conversation-context.schema.json`; state the accessible corpus and coverage boundary; classify EXPLICIT, CONFIRMED_PREFERENCE, INFERRED, PROPOSED, UNKNOWN and SUPERSEDED; trace source/context → CTX/REQ → owner/artifact → change → dependencies → tests/evidence → release disposition; map private/GitHub source gaps; identify affected tests and stale evidence; and report private save/read-back, GitHub commit/PR/CI/merge, host invocation, external AI, Remotion, media QA, rights and human approval separately.

Conversation context is not clinical evidence, campaign-fact verification, permission, identity or test evidence. If raw history is inaccessible, mark coverage PARTIAL_WITH_DISCLOSED_BOUNDARY; do not claim exhaustive history. If this preflight cannot be produced, mark NOT_RUN and do not imply PASS.

S14 is cross-cutting and does not replace M00 orchestration, S02 health authority, S12 independent QA or authorized human approvals.
