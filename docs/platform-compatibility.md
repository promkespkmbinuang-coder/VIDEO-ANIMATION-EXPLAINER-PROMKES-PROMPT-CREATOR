# Cross-platform portability and adapter policy

## Canonical source

`skills/<skill-name>/SKILL.md` is the only editable source of truth. Each SKILL.md has YAML frontmatter with unique `name` and a use-oriented `description`. Supporting files are referenced relative to that skill directory. Platform export folders are generated copies; do not edit exports directly.

## Candidate discovery layouts

| Platform/surface | Candidate skill folder | Status in this release |
|---|---|---|
| Agent Skills-compatible hosts | `skills/` (package canonical) | Format-oriented; runtime depends on host |
| OpenAI Codex | `.agents/skills/` | Export adapter provided; not runtime-tested here |
| Claude Code | `.claude/skills/` | Export adapter provided; not runtime-tested here |
| GitHub Copilot | `.github/skills/` | Export adapter provided; host/version behavior not runtime-tested here |
| Gemini CLI | `.gemini/skills/` and/or `.agents/skills/` | Export adapter provided; not runtime-tested here |
| Cursor | `.cursor/skills/` | Export adapter provided; not runtime-tested here |
| VS Code agent mode | `.github/skills/` and compatible agent skill folders | Export adapter provides `.github/skills/`; not runtime-tested here |

These are discovery/layout mappings, not proof of equivalent tool use, subagent orchestration, context loading, persistence, or runtime behavior. Check current official documentation for the target version before deployment.

## Adapter design

1. Preserve canonical SKILL.md content; only folder placement differs.
2. Generate copies with `scripts/export_platforms.py`.
3. Keep tool calls optional and host-native; this package requires no MCP server or API.
4. Do not assume a target host has image understanding, web browsing, file reading, video generation, or agent delegation.
5. If a required capability is absent, downgrade to a clearly labelled text/manual workflow or mark that output portion `BLOCKED`.
6. Target-specific model prompt parameters may only be emitted after checking the named model's current official capability documentation.
7. Dynamic validation must record host/product, version, configuration, input fixture, actual output, and test outcome.

## Official references

- OpenAI Codex skills: https://developers.openai.com/codex/skills/
- Anthropic Agent Skills: https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview
- GitHub Copilot Agent Skills: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- VS Code Agent Skills: https://code.visualstudio.com/docs/copilot/customization/agent-skills
- Gemini CLI skills: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md
- Cursor Agent Skills: https://cursor.com/docs/skills

Cursor's current official documentation describes project skill locations including `.agents/skills/` and `.cursor/skills/`. The exporter retains `.cursor/skills/` as the host-specific location. See [Cursor Agent Skills](https://cursor.com/docs/skills).

Links and folder conventions can change. Re-check official documentation before making compatibility claims for a future release. A package export is not an installation or runtime test.
