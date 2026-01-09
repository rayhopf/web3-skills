# web3-skills

Collection of Web3 and blockchain data analysis skills for AI agents.

## Skills

- **[dune](skills/dune/)** - Query and analyze blockchain data using Dune Analytics Python SDK

## Usage

Skills can be loaded by AI agents that support the Agent Skills format. Each skill directory contains a `SKILL.md` file with metadata and instructions.

## Development Setup

Create a virtual environment and install development dependencies (includes `skills-ref` validator):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Validation

### Automatic Validation (Post Hook)

When working in Claude Code, skills are automatically validated after any changes to the `skills/` directory. The validation hook will:
- Detect changes to skill files
- Run `skills-ref validate` on all skills
- Display validation results in the console

The hook configuration is in `.claude/settings.json` and the validation script is at `.claude/hooks/validate-skills.sh`.

### Manual Validation

You can also manually validate skills using the `skills-ref` CLI:

**Validate a specific skill:**
```bash
skills-ref validate skills/dune
```

**Validate and show properties:**
```bash
skills-ref read-properties skills/dune
```

**Generate agent prompt XML:**
```bash
skills-ref to-prompt skills/dune
```

The validator checks:
- SKILL.md file exists
- Valid YAML frontmatter with required fields (name, description)
- Skill name matches directory name
- Name format is lowercase and follows naming conventions

## Contributing

When adding a new skill:
1. Create a directory in `skills/` with a lowercase name
2. Add a `SKILL.md` file with YAML frontmatter containing `name` and `description`
3. Run `skills-ref validate skills/your-skill` to verify the skill is valid
4. Add the skill path to `.claude-plugin/marketplace.json`
