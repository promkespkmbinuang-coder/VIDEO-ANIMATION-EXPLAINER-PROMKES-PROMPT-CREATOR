# Master Continuity Guide — canonical integration pack V4.1.6

One project-level MCG manifest registers exactly seven modular Guide modules and three protocols. It indexes owner-authored content; it does not duplicate domain source content.

| Guide | Sole primary owner |
|---|---|
| GUIDE-01 Master Character Guide | S05 visual-identity-art-direction |
| GUIDE-02 Character Personality & Narrative Profile | S04 story-screenplay-architect |
| GUIDE-03 Master Visual Style Guide | S05 visual-identity-art-direction |
| GUIDE-04 Master Narrative Style Guide | S04 story-screenplay-architect |
| GUIDE-05 Master Voice & Audio Guide | S09 voice-sound-design |
| GUIDE-06 Master World & Environment Guide | S05 visual-identity-art-direction |
| GUIDE-07 Scene Continuity Guide | S13 continuity-guardian |

S13 owns the MCG index, Guide registry, protocol refs, lock/change index and GUIDE-07 integration only. S02 exclusively owns health claim text, evidence interpretation, safe wording and Fact Lock.

Three protocols: GCL-01 Global Continuity Lock; CCM-01 Continuity Change Management; CQA-01 Continuity Quality Assurance.

Mandatory sequence: S06 storyboard → S07 motion + S09 audio/time refs + S10 edit context → S13 refresh GUIDE-07/MCG → validate locks/dependencies/scene contracts → S08 still/reference compilation. Affected scenes remain BLOCKED until S13 refresh is evidenced PASS. Still prompts describe one captured state; temporal motion remains S07-owned. Video-generator features require exact provider/model/version evidence.

Health Truth Preservation: MCG stores claim IDs, status, source/evidence refs and hashes only. It never copies or rewrites health facts. Adaptive classes are IMMUTABLE, CONTROLLED_VARIATION and SCENE_DEPENDENT. LOCKED needs authorized human approval bound to exact artifact hash, version and scope.

Schema: ../../schemas/v4/mcg-manifest.schema.json. DRAFT sample: mcg-manifest.example.json. Seven Guide templates: guides/. Three protocols: protocols/. Semantic validator: ../../scripts/validate_mcg_manifest.py.
