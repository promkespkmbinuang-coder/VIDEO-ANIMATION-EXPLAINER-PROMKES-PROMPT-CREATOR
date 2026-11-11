# Contributing

## Non-negotiable design rules

1. Preserve the user's original intent: a poster plus caption should be sufficient for the standard workflow.
2. M00 is the only integrator. Each S-skill owns one domain and sends a structured handoff.
3. Do not merge ownership domains or duplicate detailed Guide content in MCG.
4. Keep `skills/` canonical. Generate platform exports; do not hand-edit divergent copies.
5. Mark source claims, observations, verified claims, assumptions, inferences, creative additions, unknowns, and conflicts distinctly.
6. Never promote an unverified health claim to fact, invent statistics, or conceal source contradictions.
7. Record version and change impact for canonical creative changes.
8. Tests not run remain `NOT_RUN` or `SPECIFICATION_ONLY_NOT_RUN`.
9. Do not claim separate-agent orchestration, video rendering, approval, publishing, or runtime compatibility without observed evidence.
10. Avoid placing personal/sensitive data, secrets, credentials, or unlicensed assets in public repositories.
11. Every test ID must map to requirements, owner skill, dependencies and outputs in `tests/traceability.json`.
12. Static package pass must never be represented as a pass for clinical, runtime, renderer or artifact quality.

## Change workflow

- Change the owning skill/reference first.
- Update its M00 registry and affected handoff contracts.
- Update relevant acceptance cases and traceability.
- Run `python -m pip install -r requirements-dev.txt` and `python scripts/validate_package.py`.
- Review platform exports and ensure they remain generated from `skills/`.
- For release-impacting changes, bump semantic version and update CHANGELOG.
- Run external link checks and record unresolved URLs.
- Record unresolved limitations and unrun target tests honestly.

## Pull requests

Include: motivation, affected requirements/skills, behavior before/after, safety impact, tests run, tests not run, evidence links, backward-compatibility notes, and migration/export impact. Do not merge a public release while publisher licensing and required dynamic evidence remain open.
