# Skill installation guide

This document explains how to use `survey-creator` with agent products such as Codex and Claude-style local skill systems.

---

## 1. What this repository provides

This repository contains:

- `SKILL.md` — the main skill definition
- `references/` — schema and logic reference material
- `templates/` — HTML template
- `validators/` — validation, rendering, repair, and pipeline scripts
- `tests/` — contract tests

You can use it either:

1. as a **skill**
2. as a **standalone toolchain**

---

## 2. Codex installation

### Option A: install into local skills directory

Place the repository at one of these locations:

- `~/.codex/skills/survey-creator`
- `~/.agents/skills/survey-creator`

Then keep the repository structure unchanged.

### Suggested setup

```bash
git clone <your-repo-url> ~/.codex/skills/survey-creator
cd ~/.codex/skills/survey-creator/validators
npm install
npx playwright install
```

### How to invoke

In Codex, reference the skill by name:

> Use `survey-creator` to generate a survey HTML page, validate the schema, render HTML, and verify payload correctness.

---

## 3. Claude / Claude Code style usage

If you use a local workflow where skills/prompts are stored as markdown toolkits, you can:

1. keep this repository as a standalone repo
2. reference `SKILL.md` from your Claude workflow
3. call the scripts in `validators/` directly from your agent tooling

Recommended approach:

- keep `SKILL.md` as the system prompt / skill body
- keep `references/` as retrieval material
- execute `validators/run_survey_creator_pipeline.py` as the main entrypoint

### Example

Your agent instruction can say:

> Read `SKILL.md`, follow the execution sequence, generate schema from user intent, validate it, render HTML, and only return the result after the pipeline succeeds.

---

## 4. Standalone usage without skill loading

Even if your agent system does not support a “skill” abstraction, you can still use the repository as a structured pipeline.

### Main command

```bash
python3 validators/run_survey_creator_pipeline.py \
  --schema /absolute/path/to/schema.json \
  --output-dir /absolute/path/to/out \
  --auto-repair \
  --fail-on-high-warning
```

### What this gives you

- repaired schema
- HTML output
- payload sample
- pipeline report

---

## 5. Required dependencies

### Python
- Python 3.10+

### Node / browser automation
- Node.js 18+
- Playwright browsers

Install with:

```bash
cd validators
npm install
npx playwright install
```

---

## 6. Recommended agent integration pattern

No matter whether you use Codex or Claude-like tooling, the best pattern is:

1. interpret user intent
2. generate internal schema
3. validate schema
4. render HTML
5. validate runtime and interaction
6. validate payload
7. only return output if `shipReady === true`

In other words:

> Do not let the agent stop at “generated schema looks fine”.  
> Always pass through the pipeline.

---

## 7. Best practice for open-source users

If you want other people to reuse this repository easily:

- keep repo structure stable
- do not rename `SKILL.md`
- do not move `references/`, `templates/`, or `validators/`
- document your supported runtimes clearly
- treat `validators/run_survey_creator_pipeline.py` as the public main entrypoint

