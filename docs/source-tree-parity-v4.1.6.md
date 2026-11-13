# Source-tree parity and identity — V4.1.6

**GitHub baseline:** 6f1445950028326d9a312f5ba2c1efee3d59ded9 (PR #18 merge).
**Proposed branch:** fix/mcg-canonical-integration-v4.1.6.

The private Plugin Creator product and GitHub repository are related but distinct package identities and source trees. This change synchronizes the MCG contract semantically; it does not claim byte-for-byte source parity or runtime parity.

| Domain | Private product | GitHub product | Treatment |
|---|---|---|---|
| S13 | continuity-guardian | continuity-guardian | Canonical role and owner map align |
| M00 | video-explainer-promkes | master-orchestrator | Orchestration role aligned; paths differ |
| S09 | voice-audio-intelligence | voice-sound-design | Same canonical S09 owner; product alias |
| S10 | renderer-code-engineering | editing-postproduction | Role boundary aligned; slugs differ |
| Gate engine | private legacy CTRL | GitHub V4-CTL candidate | Remains NOT_SYNCED pending review |

Do not copy binary/Remotion assets or gate-engine implementations across products without rights review, explicit authorization, independent technical review and hash-based parity evidence. Repository visibility is not a license.
