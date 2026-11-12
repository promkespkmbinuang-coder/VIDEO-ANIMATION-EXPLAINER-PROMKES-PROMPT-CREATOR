# Skill source parity matrix — GitHub vs private Plugin Creator

**Audit date:** 2026-11-12. This is a semantic mapping inventory, not proof that files are byte-identical or behaviorally equivalent.

| GitHub skill path | Private Plugin Creator skill path | Mapping status |
|---|---|---|
| skills/master-orchestrator | skills/video-explainer-promkes | INTENTIONAL_SLUG_DIVERGENCE; M00 ownership matches conceptually, body/version parity requires review |
| skills/source-asset-intelligence | skills/source-asset-intelligence | SAME_SLUG; verify content parity separately |
| skills/health-evidence-safety-auditor | skills/health-evidence-safety-auditor | SAME_SLUG; verify content parity separately |
| skills/audience-campaign-strategy | skills/audience-campaign-strategy | SAME_SLUG; verify content parity separately |
| skills/story-screenplay-architect | skills/story-screenplay-architect | SAME_SLUG; verify content parity separately |
| skills/visual-identity-art-direction | skills/visual-identity-art-direction | SAME_SLUG; verify content parity separately |
| skills/storyboard-cinematography | skills/storyboard-cinematography | SAME_SLUG; verify content parity separately |
| skills/animation-motion-design | skills/animation-motion-design | SAME_SLUG; verify content parity separately |
| skills/ai-video-reference-engineering | skills/prompt-reference-video-engineering | INFERRED_SEMANTIC_MAPPING; both describe still/reference prompt compilation, owner confirmation required |
| skills/voice-sound-design | skills/voice-audio-intelligence | INFERRED_SEMANTIC_MAPPING; both describe audio intake, transcript, VO, subtitle and sound design, owner confirmation required |
| skills/editing-postproduction | skills/renderer-code-engineering | CONSOLIDATED_S10_SCOPE; one S10 owner covers editing/post-production plus renderer/code/render/export; slug divergence is intentionally preserved; verify content parity by read-back/hash before marking fully SYNCED |
| skills/social-accessibility-distribution | skills/social-accessibility-distribution | SAME_SLUG; verify content parity separately |
| skills/quality-assurance-controller | skills/quality-assurance-controller | SAME_SLUG; verify content parity separately |
| skills/continuity-guardian | skills/continuity-guardian | SAME_SLUG; verify content parity separately |
| skills/conversation-release-audit | skills/conversation-release-audit | SAME_SLUG; verify content parity separately |

## Private-only operational helper

- Private package: skills/executable-gate-engine/SKILL.md
- GitHub main/PR branch: no equivalent skill path was found in the inspected tree.
- Status: PRIVATE_PACKAGE_ONLY / SOURCE_PARITY_GAP. Do not call it S15; do not claim GitHub source parity until a deliberate decision is made to publish, rename, or keep it private.

## Rules

1. Same slug is not proof of same content; compare file hashes or full text before marking SYNCED.
2. INFERRED_SEMANTIC_MAPPING requires human owner confirmation before a rename, merge or removal.
3. Preserve both sides until migration impact and downstream references are tested.
4. Do not copy private-only binary assets or operational material to public GitHub without rights and publication review.
5. Version equality does not imply source-tree parity.
