# Release Guide

This project uses lightweight source releases.

## Pre-Release Checks

Run from the repository root:

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_workflow_pack.py examples/complete-run
git diff --check
git status --short
```

Check that:

- `README.md` and `README.en.md` describe the same workflow state.
- `workflow/contract.json` matches `docs/workflow-contract.md`.
- `examples/complete-run/` passes the validator.
- `.env` or real API keys are not present in tracked files.

## Tagging

Only tag after the user explicitly approves a release.

```bash
git tag -a vX.Y.Z -m "vX.Y.Z"
git push origin main
git push origin vX.Y.Z
```

Do not force-push release tags.
