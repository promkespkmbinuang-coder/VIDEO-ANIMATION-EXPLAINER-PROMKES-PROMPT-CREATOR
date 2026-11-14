# Comparative adoption audit — Claude Remotion Skill → Video Explainer Promkes V4.1.11

**Disposition:** additive design adoption; target runtime and final production release remain separately gated.

## 1. Scope and evidence boundary

Compared the public repository `haidrrrry/claude-remotion-skill` (main tip inspected at `1dcbe5e3fc6cf970bd10d3cc05f0a8a5d19d0383`) with the Promkes public repository (`promkespkmbinuang-coder/VIDEO-ANIMATION-EXPLAINER-PROMKES-PROMPT-CREATOR`, main baseline inspected at `8b3fe9f09ac0f193e49ae7df36937668e69c065d`) and the private account plugin source inventory/read-back for V4.1.10. This audit inspected source documents, relevant skills, manifests, schemas, examples, reports and repository metadata. It did not execute a full Claude workflow, install Remotion from npm, run live ChatGPT plugin invocation, inspect new MP4 media or authenticate human approvals. Historical package reports are treated as historical records, not fresh tests.

S14 coverage is bounded to the current conversation, available conversation summaries, current source read-back and GitHub data retrieved in this audit; it is not a claim that every raw historical conversation was reopened. Public repository name/identity and private plugin identity remain distinct; matching version numbers do not establish source-tree or byte parity.

## 2. Comparative findings

Claude Remotion Skill is stronger as an immediately usable motion-design cookbook: its source separates a concise master workflow, 17 practical patterns, design rules, a shared theme template, example compositions and a render/inspect/fix loop. It provides concrete approaches for entrances, stagger, text reveals, moving backgrounds, grade/grain/vignette, Ken Burns, counters, radial accents, exits, micro-motion, parallax, transitions, blur, audio cues and synchronized captions.

Promkes is stronger as a governed production system: it has exclusive ownership across S01–S14, S02 health-truth authority, S05 visual canon, S06 camera/shot ownership, S07 quantified renderer-neutral motion, S09 audio provenance/timing, S10 capability-bound renderer mapping, S11 accessibility/distribution, S12 independent QA, S13 MCG/Guide continuity and mandatory S14 release-context preflight. It also has motion schemas, fail-closed adapter behavior, asset rights handling, risk routing and layered release gates.

The appropriate outcome is not to replace Promkes with the smaller Claude structure. It is to add a tested and optional pattern catalogue to S07, map only supported patterns through S10, and add independent S12 verification.

## 3. Positive features selected for adoption

- Reusable entrance, stagger, phrase reveal, background depth, grade, grain, vignette, Ken Burns, counters, radial accents, exits, micro-motion, parallax, transition and blur patterns.
- Centralized visual tokens, with S05/Guide-03 remaining their source of truth.
- Audio-linked movement and caption pattern concepts, with S09 retaining source/timing/rights ownership.
- Concrete pattern examples as design references and test fixtures rather than mandatory output style.
- Explicit render → inspect → fix → re-render as an iterative quality process.
- Portable still-frame inspection as one inspection option, not a substitute for encoded-media inspection.
- Reproducible procedural generation as a requirement where synthetic assets are used, with seeded generation and recorded configuration.

## 4. Negative findings converted to controls

| Finding | Failure mechanism | Adopted control |
|---|---|---|
| Inconsistent interpolation guidance | A pattern silently conflicts with master rules | Explicit easing and boundary contract; deliberate linear intent is permitted only when documented and bounded |
| Universal design rules | Forced motion can harm comprehension/accessibility | Pattern choice is conditional; static holds and reduced-motion variants remain valid |
| No explicit capability gate | Code/render may be claimed without actual runtime | S10 capability matrix and route selection required before target-specific code/render claims |
| Source frame and MP4 QA conflated | Source frame does not reveal encode/export defects | Separate composition-frame QA and encoded-media QA |
| Nondeterministic procedural audio | Same inputs can yield different output | Seeded generation where deterministic outputs are required; record parameters and generator version |
| Unpinned/weak dependency assurance | Reproduction can drift | Retain exact package version contract, lockfile and version verification as release requirements |
| Composition/docs drift | Documented command may point to absent composition | Composition inventory and docs/script parity checks required |
| Non-atomic ZIP build | Failed rebuild may lose previous artifact | Build temporary archive, verify CRC/content, atomically replace only after success |
| Limited rights/asset governance | Pattern examples may encourage unlicensed reuse | S01/S13 asset provenance, rights, consent and lifecycle checks remain mandatory |
| Incomplete recovery | Failed render may overwrite or leave ambiguous output | Preserve prior artifact, bounded retries, logs, CHG-ID and invalidation/retest |

## 5. Explicitly not adopted as universal rules

Do not mandate linear-free movement without exceptions, a five-layer stack in every scene, one hero colour or glow per frame, every still using Ken Burns, every element breathing, a fixed movement cadence, or 2–3 animated properties on every entrance. These are useful stylistic options only when they fit the narrative, brand, audience, health literacy, reduced-motion and technical constraints.

Do not infer support for arbitrary Remotion patterns from the existence of the pattern library. The inspected Promkes Remotion V3 adapter profile remains limited to a single selected/approved still per scene, editable React text overlays, sequential `Sequence`, cut-only transitions and one centered scale-only motion record per scene (scale range 1.0–1.15). Audio, subtitle, crossfade, arbitrary path, multiple references, dynamic URLs and AI video generation remain unsupported by that profile until a separately tested adapter is supplied.

## 6. Ownership and data flow

`S05 visual tokens/Guide-03 → S06 storyboard/camera intent → S07 selected pattern + quantified motion record → S13 continuity refresh/locks → S10 exact renderer mapping + mapping-loss report → S12 independent package/render/media QA`.

S09 supplies audio and timing provenance; S02 retains exclusive health fact authority; S11 supplies accessibility/distribution requirements. M00 orchestrates and preserves the existing gates. No new specialist or duplicate production gate is introduced.

## 7. Acceptance and verification boundary

The twelve `RMP-AC-*` conditions are defined in `skills/animation-motion-design/references/remotion-pattern-adoption-v4.1.11.md`. Static source/contract checks can validate the catalogue and routing references only. They cannot prove that the host invoked the plugin, npm dependencies installed, Remotion Studio opened, a target composition bundled, a render succeeded, an MP4 was inspected, audio was heard, or human approvals were obtained.

The last inspected private package report recorded npm registry `EAI_AGAIN`, Remotion dependency installation `BLOCKED`, Studio/render/media QA `NOT_RUN`; that is a historical report, not a fresh test in this update. Current target CI and runtime evidence must be fetched and tested against the actual candidate commit/release. Any absent evidence remains `NOT_RUN`, `NOT_VERIFIED` or `BLOCKED`.

## 8. Release/parity notes

- Private account plugin identity remains `video-explainer-promkes-renderer-engine`; public repository root manifest keeps its existing product name `video-animasi-explainer-promkes-prompt-creator` pending owner-confirmed identity reconciliation.
- Private source path `skills/renderer-code-engineering` and GitHub source path `skills/editing-postproduction` are not silently declared byte-identical. Preserve the mapping as a known source-tree divergence.
- Existing MCG, Guide and protocol ownership, R0–R3 routing, S14 preflight, rights/consent controls and health Fact Lock remain intact.
- A saved private plugin release, a GitHub branch/PR, CI, target runtime, MP4 QA and human/publication approvals are separate status records.


## Concurrent GitHub change and release boundary

At this audit's GitHub publication checkpoint, pull request #26 (`feat/v4.1.9-learning-asset-operationalization`) is OPEN and DRAFT against the same `main` baseline. It changes the root/Codex manifests, README, CHANGELOG, M00 and S12 among other files. This motion-pattern branch deliberately does not change those overlapping paths. The public root manifest remains at its baseline version in this branch; this is a source proposal, not a claim that public `main` has been released as V4.1.11. Reconcile version manifests, README/changelog and source parity after PR #26 is independently reviewed and its disposition is known.
