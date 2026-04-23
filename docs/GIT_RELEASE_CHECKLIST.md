# Git release checklist

Use this checklist before pushing `survey-creator` to GitHub.

---

## 1. Repository hygiene

- [ ] Confirm repository name
- [ ] Confirm public description/tagline
- [ ] Confirm visibility: public / private
- [ ] Confirm `LICENSE` is correct
- [ ] Replace placeholder copyright holder if needed
- [ ] Confirm `.gitignore` is present
- [ ] Ensure no local absolute paths remain
- [ ] Ensure no private machine-specific output files remain

---

## 2. Files that should exist

- [ ] `README.md`
- [ ] `LICENSE`
- [ ] `SKILL.md`
- [ ] `references/`
- [ ] `templates/`
- [ ] `validators/`
- [ ] `tests/`
- [ ] `docs/GITHUB_OVERVIEW.md`
- [ ] `docs/SKILL_INSTALLATION.md`
- [ ] `docs/GIT_RELEASE_CHECKLIST.md`
- [ ] `examples/minimal-survey.json`

---

## 3. Files that should NOT be committed

- [ ] `evals/**/outputs/`
- [ ] local temp directories
- [ ] browser temp output
- [ ] `.DS_Store`
- [ ] `node_modules/`
- [ ] ad-hoc generated HTML/payload/report files unless intentionally included as examples

---

## 4. Dependency readiness

- [ ] `validators/package.json` is present
- [ ] `validators/package-lock.json` is present if you want reproducible installs
- [ ] install instructions in `README.md` are correct
- [ ] Playwright install instructions are correct

---

## 5. Validation before push

Run:

```bash
./run_all_legality_checks.sh
```

Before release, confirm:

- [ ] reference consistency passes
- [ ] contract tests pass
- [ ] smoke tests pass
- [ ] final output shows `shipReady: YES`

---

## 6. GitHub page readiness

- [ ] Add repository description
- [ ] Add topics/tags
- [ ] Pin key docs in README
- [ ] Add homepage URL if you have one
- [ ] Decide whether to enable Issues
- [ ] Decide whether to enable Discussions
- [ ] Decide whether to add contribution guide later

Suggested topics:

- `survey`
- `form-generator`
- `ai`
- `schema-validation`
- `playwright`
- `html`
- `questionnaire`
- `agent-skill`

---

## 7. Suggested first commit flow

```bash
git init
git add .
git commit -m "feat: open source survey-creator"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

---

## 8. Suggested post-publish checks

After pushing:

- [ ] Clone the repo into a clean directory
- [ ] Re-run installation steps from README
- [ ] Re-run `./run_all_legality_checks.sh`
- [ ] Re-run the minimal example pipeline
- [ ] Verify README instructions work exactly as written

---

## 9. Recommended first public message

When announcing the project, explain clearly:

- what problem it solves
- why it is different from simple HTML form generators
- that it includes legality and payload validation
- that it is suitable for AI-driven survey creation workflows

