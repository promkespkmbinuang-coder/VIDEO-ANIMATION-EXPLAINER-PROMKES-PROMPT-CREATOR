# Release audit snapshot — V4.0.8

**Audit date:** 2026-11-12 (Asia/Makassar). Coverage is partial: current conversation, available prior-conversation summaries, private Plugin Creator read-back and selected GitHub PR/CI evidence.

## Corrections
- The V4.0.7 GitHub CI failure at run #158 still showed the import before sys.path insertion; that run predates the corrected commit 1de773d.
- The package validator now disables bytecode writes before importing its release validator, preventing the validator from generating a cache file that it then rejects.
- The workflow disables pytest bytecode/cache generation and removes the obsolete build/v4-blocked-gate-report.json artifact path; the actual report is build/v4-release-gate.json.
- Private Plugin Creator contains 16 skill files: 15 numbered modules plus executable-gate-engine helper. GitHub source has 15 numbered modules; the helper is an intentional private-package divergence.

## Skill source parity\nSee docs/skill-source-parity-matrix.md. Three slug mappings remain inferred and require owner confirmation; executable-gate-engine is private-package-only and has no inspected GitHub equivalent.\n\n## Latest CI finding at audit time\nRun #171 failed before pytest: package validator's skill-name registry used private-package slugs instead of the actual GitHub slugs, and claim-record.schema.json contained a malformed duplicate allOf block. The current PR branch corrects both; only a fresh run on the exact latest head can establish whether the fixes pass.\n\n## Evidence boundary
The corrected PR head must receive fresh CI. Earlier failures #148 and #158 are evidence for earlier heads only. Main merge commit PR #13 remains without verified post-merge CI. No independent reviewer submission has been recorded for PR #14.

No LICENSE is added. GitHub repository remains PUBLIC; Plugin Creator remains PRIVATE. Live ChatGPT invocation, external AI/ASR/TTS, Remotion install/Studio/bundle/render, MP4 QA, clinical/legal/rights/privacy/brand/accessibility and final human release approvals remain NOT_RUN, NOT_VERIFIED or BLOCKED. Production/public release remains HOLD.
