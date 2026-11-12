# GitHub source publication and release governance

## Canonical destination

Repository target: [`promkespkmbinuang-coder/VIDEO-ANIMATION-EXPLAINER-PROMKES-PROMPT-CREATOR`](https://github.com/promkespkmbinuang-coder/VIDEO-ANIMATION-EXPLAINER-PROMKES-PROMPT-CREATOR)

Default branch: `main`. The complete Prompt-to-Reference source package is prepared for a review branch first. Do not equate branch publication with a merged, licensed, tested, or approved public release.

## Required source layout

The repository must contain the package root: root and compatibility manifests, canonical `skills/`, all seven Guide definitions/templates, `docs/`, `tests/`, `scripts/`, requirements, and `.github/workflows/`. The source count must be measured from the current package inventory rather than relying on the obsolete historical figure of 50 files.

## License and rights gate

No license is selected in this release. Repository visibility alone does not grant permission to reuse, modify, redistribute, or commercially exploit the source. Before adding a LICENSE file or tagging a public release, the publisher must review ownership and third-party rights for all source text, templates, fonts, images, logos, examples, health materials, and any bundled assets; then choose and approve a suitable license. Until that decision is recorded, treat the package as **all rights reserved by default; no open-source license is granted**. This wording is a rights notice, not a substitute for legal review or a selected OSI license.

## CI gates

- `validate.yml`: strict YAML parsing, both manifests, folder/frontmatter naming, local Markdown/supporting references, suite counts, and one-to-one traceability coverage.
- `links.yml`: external and local Markdown URL verification with lychee.
- CI must run on push and pull request. Retain workflow run IDs and uploaded validation summaries as evidence.
- A green static workflow is necessary but not sufficient for public release.

## Release approval checklist

- [ ] Full source tree is visible on the intended review branch and every file is readable.
- [ ] Static validator passes on GitHub Actions.
- [ ] Markdown/external-link workflow passes or approved exceptions are documented.
- [ ] Publisher identity and author metadata are consistent.
- [ ] Asset provenance and third-party ownership have been reviewed.
- [ ] Publisher explicitly chooses the license and approves the LICENSE text.
- [ ] The 45 baseline and 13 reference acceptance cases have actual execution evidence or remain visibly NOT_RUN.
- [ ] Each target host, external reference model and downstream renderer is tested separately.
- [ ] Actual video/audio/subtitle/overlay artifacts pass S12 and human review.
- [ ] Changelog, version, tag, release notes and residual unknowns are synchronized.
- [ ] Maintainer approves merge to `main` and any public release announcement.

## Release policy

No tag or public-directory readiness claim while the license decision, external runtime tests, downstream artifact QA, or human approval remains open. A review branch or pull request is a source-review checkpoint only.


## V4.0.4 — conversation audit and release parity addendum (2026-11-12)

- M00 + S01–S14 includes S14 for conversation coverage, explicit/inferred/proposed/unknown context classification, cross-release traceability and publication evidence.
- Run `python scripts/validate_release_consistency.py --root .` in CI. It rejects duplicate JSON keys, root/Codex manifest drift, README/version drift and missing current changelog entries.
- PR #7 is **merged** (merge commit `11e9d0c746d11934eadf8caa50aa12550b8eceaa`). Its successful CI run IDs `43212943964` and `43212943521` refer to PR head `ad8013ccfe4dbfa92a91cd4751cd0c30316bca27`, not a new run on the merge commit.
- Private Plugin Creator V4.0.4 source read-back is separate from GitHub sync and ChatGPT installation.
- Full private-plugin/GitHub tree parity remains **NOT_RECONCILED**; the private package contains Remotion adapter files/assets not found in the inspected GitHub main tree.
- Public production release remains **HOLD** while runtime, media QA, rights, clinical/legal/privacy/accessibility and human approvals are open. Do not add a license without an explicit rights-holder decision.
