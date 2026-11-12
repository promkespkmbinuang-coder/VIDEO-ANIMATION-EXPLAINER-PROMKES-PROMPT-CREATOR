# Release audit snapshot — V4.1.0 candidate

**Audit date:** 2026-11-12 (Asia/Makassar). Coverage includes this conversation, available prior-conversation summaries, current private Plugin Creator read-back, selected GitHub source files, PR metadata and workflow logs. Raw full text of every historical conversation is not available; conversation coverage is **PARTIAL_WITH_DISCLOSED_BOUNDARY**.

## Accepted continuity requirements

- Preserve poster/image-first, audio-first, transcript-first, script-first and hybrid intake.
- Keep health evidence, claim traceability, Fact Lock, ethical campaign/story/CTA, visual continuity, storyboard/motion, reference prompts, audio/transcript/subtitle, renderer handoff, independent QA and release-state boundaries.
- Treat Polewali Mandar dialect and “Halo Sola Seha’” as optional brief/brand-profile choices; never globalize one-off DBD/TBC/fogging campaigns, dates, locations, institutions, statistics or CTAs.
- A static poster's 4:5 aspect ratio/logo margins do not set video dimensions.
- Keep the 1,000 generated candidate definitions explicitly NOT_RUN and NOT_VERIFIED; they are not 1,000 executed tests.
- Keep S14 mandatory before conversation audit, versioned changes, source reconciliation, GitHub publication and release decisions.

## S10 source parity resolution

S10 is one owner with two complementary capability lanes:
1. Editing/post-production: timeline assembly, pacing, transitions, overlays, subtitle/audio integration, mix/mastering where supported and export preparation.
2. Renderer/code engineering: renderer-neutral composition contract, target adapter, typed props, code, project assembly, runtime checks, render/export and artifact verification.

S09 retains source-audio intelligence, transcript provenance, segmentation, timing, VO direction and sound-design specifications. S10 assembles approved material in the timeline. S11 owns accessibility/distribution; S12 independently evaluates. GitHub keeps the slug `editing-postproduction`; private Plugin Creator keeps `renderer-code-engineering`. This is an intentional slug divergence, not a capability deletion or a second S10 owner.

## Gate-engine hardening in this candidate

- Completes the Ed25519 verifier's valid-key path; malformed key/signature returns explicit failure.
- Removes a malformed unused helper and the earlier CLI entrypoint that exited before the active CLI definition.
- Makes transitive invalidation deterministic and return its sorted dependent IDs; adds an active non-destructive `apply-invalidation` CLI path that writes a new snapshot.
- Aligns artifact-envelope fixtures and manifest path validation with the required `content_path` field.
- Makes the legacy diagnostic evaluator fail closed for TEST_FIXTURE/non-production projects. A synthetic fixture cannot become production-release eligible.
- Keeps the 21 active V4-CTL controls distinct from the legacy CTRL diagnostic registry pending a future single-registry cleanup.

## Evidence and blockers

- Private Plugin Creator V4.1.0 is VERIFIED by save/read-back: release ID `pluginrel_6af5cf26722081918100567dee41059c`, scope USER, discoverability PRIVATE; root/Codex manifests, README, CHANGELOG, release-audit and S10 skill file are present.
- GitHub PR #14 is the source-publication vehicle, based on main `6aa128ebaa8d561fcedf7a52f027bd2a2a931198`; keep it Draft until fresh CI on its exact latest head is green and independent review is recorded.
- Historical validate-package run #184 on older head `f08c201249afed417e270d695d10f7279f9d47ec` logged 31 failures / 58 passes. It is stale for the current PR head and must not be presented as current validation. Link-check #188 was successful on that older head only.
- On PR head `8b570f7454f60373f99c525806efe2718bd50b5f`, validate-package run #223 (ID `43239351709`) and markdown-link-check run #227 (ID `43239351687`) both completed SUCCESS. Pytest: **89 passed in 1.35s**; strict package/traceability validation, schema/semantics, active controls, pre-release gate smoke, blocked-fixture CLI and evidence upload all completed successfully.
- The immediately preceding validate run #219 on SHA `19a3de6853339acfbd89eb5057c3ebe36bd2dc37` had 88 passed / 1 failed due the coverage test still asserting an obsolete test name; the assertion was updated in the subsequent commit. Runs #223/#227 above are the latest verified pair for the pre-audit-note head; any later head requires its own fresh CI.
- Direct push/main CI on the current main SHA remains NOT_VERIFIED unless a workflow event/ref/SHA explicitly proves it.
- No LICENSE is added: repository visibility PUBLIC is not a license or rights grant. Publisher must decide ownership, third-party asset rights and any license before public redistribution.
- Reviewer identity/authority, clinical/legal/rights/privacy/brand/accessibility approvals, live ChatGPT invocation, external AI/ASR/diarization/TTS, Remotion install/Studio/bundle/render, MP4 decoding/perceptual QA and final human release approval remain NOT_RUN, NOT_VERIFIED or BLOCKED.
- The Ed25519 verifier only proves a signature against the supplied key. The trusted-key registry must be independently protected and institutionally administered; a key supplied inside the same project payload does not authenticate a real person's identity, role or authority.

**Disposition: SOURCE-CANDIDATE / CI-PENDING / REVIEW-PENDING / PRODUCTION-PUBLIC-RELEASE-HOLD.** No merge, tag, deployment, public plugin publication or human approval is implied.
