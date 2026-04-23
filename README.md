# survey-creator-skill

[English](./README.md) | [简体中文](./README.zh-CN.md)

**Schema-safe survey generator and legality pipeline for AI-driven questionnaire creation.**

`survey-creator-skill` is an open-source skill + toolchain for building production-safe survey experiences from structured schema.

It does more than render HTML:

- validates survey schema legality
- repairs safe schema issues
- renders submittable HTML survey pages
- verifies runtime behavior in browser E2E
- checks interaction flow
- validates accessibility
- validates payload contract
- guarantees submitted payloads match the exact survey schema

If you want AI to generate questionnaires **without silently producing invalid forms or broken submit payloads**, this project is built for that.

---

## Why this project exists

Most “AI form generators” stop at:

- generate some JSON
- render some HTML
- hope the submit data is usable

That is usually not enough for real delivery.

Survey and questionnaire systems have stricter needs:

- schema must be legal
- ids must be stable and unique
- logic must not break required validation
- hidden/skipped questions must not leak into payload
- runtime must not blank-screen
- rendered form should be browser-testable
- submit payload must match the concrete survey definition

`survey-creator-skill` is designed around that full chain.

---

## What it includes

### Skill layer
- `SKILL.md`
- structured generation workflow
- schema-first output discipline
- legality-first delivery rule

### Reference layer
- schema notes
- field guides
- rich text rules
- pagination rules
- child input rules
- local cache rules
- logic rules
- logic final specification
- logic example library
- submission contract

### Runtime layer
- frozen HTML template
- client-side step flow
- logic runtime
- cache handling
- payload assembly

### Validation layer
- schema validation
- schema auto-repair
- HTML runtime validation
- HTML E2E validation
- HTML interaction E2E validation
- accessibility validation
- payload validation
- payload-against-schema validation

### Quality layer
- contract tests
- smoke tests
- full legality checks

---

## Supported question types

- `radio`
- `checkbox`
- `input`
- `score`
- `nps`
- `survey`
- `finish`
- `Pagination`

---

## Supported logic operators

- `selected`
- `not_selected`
- `contains`
- `not_contains`
- `exists`
- `not_exists`
- `answered`
- `not_answered`
- `eq`
- `neq`
- `gt`
- `lt`

## Supported logic actions

- `show_question`
- `hide_question`
- `show_option`
- `hide_option`
- `auto_select_option`
- `jump_to_question`
- `jump_to_page`
- `end_survey`

---

## Logic guarantees

This project already enforces these runtime rules:

- **hidden = nonexistent**
- **skipped = nonexistent**
- hidden/skipped questions do not block required validation
- hidden/skipped questions do not enter payload
- hidden/skipped questions are removed from cache
- hidden options are cleared from state
- conflicting rules resolve by declaration order
- later matched logic overrides earlier matched logic
- auto-select only applies to final visible targets

---

## Best use cases

- AI-generated surveys
- registration questionnaires
- screening / qualification forms
- customer satisfaction research
- NPS / score workflows
- AI Native form creation flows
- teams that need stronger legality guardrails before shipping HTML questionnaires

---

## Repository structure

```text
survey-creator-skill/
  SKILL.md
  README.md
  LICENSE
  examples/
  references/
  templates/
  validators/
  tests/
  evals/
  docs/
  run_all_legality_checks.sh
```

---

## Requirements

### Runtime
- Python 3.10+
- Node.js 18+

### Browser automation
- Playwright

---

## Install

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd survey-creator-skill
```

### 2. Install validator-side dependencies

```bash
cd validators
npm install
npx playwright install
cd ..
```

Python validators currently rely on the standard library, so no separate Python package install is required.

---

## Quick start

Run the full legality pipeline on the bundled example:

```bash
python3 validators/run_survey_creator_pipeline.py \
  --schema examples/minimal-survey.json \
  --output-dir ./out \
  --auto-repair \
  --fail-on-high-warning
```

This produces:

- repaired schema
- rendered HTML
- generated payload sample
- pipeline report

---

## Run all checks

```bash
./run_all_legality_checks.sh
```

This runs:

- reference consistency check
- contract tests
- validator smoke tests

Only treat the repo as healthy when this command passes.

---

## Standalone usage

### Validate schema

```bash
python3 validators/validate_survey_schema.py /absolute/path/to/schema.json
python3 validators/validate_survey_schema.py /absolute/path/to/schema.json --json
```

### Render HTML

```bash
python3 validators/render_survey_html.py \
  --schema /absolute/path/to/schema.json \
  --out /absolute/path/to/output.html
```

### Full pipeline

```bash
python3 validators/run_survey_creator_pipeline.py \
  --schema /absolute/path/to/schema.json \
  --output-dir /absolute/path/to/output-dir \
  --auto-repair \
  --fail-on-high-warning
```

### Validate payload

```bash
python3 validators/validate_survey_payload.py /absolute/path/to/payload.json
python3 validators/validate_payload_against_schema.py \
  /absolute/path/to/schema.json \
  /absolute/path/to/payload.json
```

### Validate rendered HTML

```bash
python3 validators/validate_survey_html_runtime.py /absolute/path/to/file.html
python3 validators/validate_survey_html_e2e.py /absolute/path/to/file.html
python3 validators/validate_survey_html_interaction_e2e.py /absolute/path/to/file.html
python3 validators/validate_survey_html_accessibility.py /absolute/path/to/file.html
```

---

## Use as a Codex skill

Copy or symlink this repository into your local skills directory:

- `~/.codex/skills/survey-creator-skill`
- `~/.agents/skills/survey-creator-skill`

Then invoke it by name in your prompt.

Example:

> Use `survey-creator-skill` to generate a survey HTML page, validate the schema, render the HTML, and verify payload correctness before returning the result.

### Use with Claude-style local workflows

You can also use this repository as a standalone skill/toolchain in Claude-style or custom agent systems:

- keep `SKILL.md` as the main skill prompt
- keep `references/` as retrieval material
- use `validators/run_survey_creator_pipeline.py` as the main executable entrypoint
- only treat output as deliverable when the pipeline returns `shipReady = true`


---

## Documentation map

### Product / project overview
- `docs/GITHUB_OVERVIEW.md`
- `docs/GIT_RELEASE_CHECKLIST.md`

### Core references
- `references/schema-notes.md`
- `references/field-guide-overview.md`
- `references/submission-contract.md`
- `references/logic-rules.md`
- `references/logic-specification.md`
- `references/logic-example-library.md`

### Validators
- `validators/README.md`
- `validators/pre-release-checklist.md`

### Tests
- `tests/contract/README.md`

---

## Open-source readiness

This repository is designed to be portable:

- repository-relative path resolution
- generated outputs ignored by `.gitignore`
- no fixed local machine path requirement
- contract-tested logic semantics
- browser-validated runtime behavior

---

## Recommended positioning

This project is best described as:

> A schema-safe survey generator and legality pipeline for AI-driven questionnaire creation.

That is more accurate than calling it only an “HTML form generator”, because the main value is not just rendering — it is **legality, logic safety, payload correctness, and pre-release validation**.

---

## License

MIT

