# Evidence-to-PPT Workflow Hardening Implementation Plan

> **For agentic workers:** REQUIRED: Use `subagent-driven-development` if the current harness supports helper agents; otherwise use `executing-plans`. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the repository from a well-documented Codex workflow specification into a verifiable, reusable open-source workflow package. The next implementation pass must add machine validation, CI, a complete passing example, install acceptance checks, and tighter rule consolidation without changing the public promise of the project.

**Architecture:** Keep the existing repository layout and add a thin validation layer around the existing workflow contract. The workflow remains a local Codex skill that orchestrates GPT Researcher, Codex source audit, claims matrix creation, and ppt-master. Validation should not call paid APIs or require model keys; it should check repository examples and user-produced workflow packs with deterministic local scripts.

**Tech Stack:** Python 3 standard library, GitHub Actions, Markdown, CSV, JSON, existing Codex skill layout.

---

## Current Findings

The repository currently has a clear Chinese default README, an English README, visual assets, examples, API key guidance, and a Codex skill file. The repository does not yet contain a validator, test suite, CI workflow, complete passing workflow pack, install smoke test, issue templates, or release tagging path.

The current `examples/example-source-table.csv` has 4 sources, while `skills/evidence-to-ppt-workflow/SKILL.md` and `docs/workflow-contract.md` stop the workflow when fewer than 5 credible sources remain. This should be preserved as a format sample only, or replaced by a passing example.

The README Roadmap still lists English README as incomplete even though `README.en.md` exists.

## Non-Goals

- Do not add a server, web UI, package manager dependency, or paid API call to validation.
- Do not store or request real API keys.
- Do not claim that the workflow guarantees factual correctness; validation only confirms traceability and contract compliance.
- Do not replace GPT Researcher or ppt-master. This repository remains an orchestration layer.

## Phase 1: Add A Single Machine-Readable Contract

- [ ] Add `/Users/sunjieqiong/Documents/Codex/2026-06-26/qin/evidence-to-ppt-workflow/workflow/contract.json`.
- [ ] Add `/Users/sunjieqiong/Documents/Codex/2026-06-26/qin/evidence-to-ppt-workflow/schemas/workflow-contract.schema.json`.
- [ ] Mirror only the stable hard gates in JSON:

```json
{
  "version": "0.1.0",
  "required_files": [
    "00_brief.md",
    "01_research_pack.md",
    "02_source_table.csv",
    "03_claims_matrix.md",
    "04_ppt_outline.md",
    "05_audit_report.md",
    "06_ppt_master_input.md"
  ],
  "source_table_headers": [
    "source_id",
    "title",
    "author_or_org",
    "date",
    "url",
    "source_type",
    "access_date",
    "claim_supported",
    "quoted_or_paraphrased_evidence",
    "reliability_tier",
    "notes"
  ],
  "credible_source_tiers": ["A", "B"],
  "minimum_credible_sources": 5,
  "claim_statuses_requiring_evidence": ["accepted", "needs caveat"],
  "ppt_master_input_required_phrases": [
    "do not introduce new factual claims not present in the approved materials",
    "不要新增未经审查事实"
  ]
}
```

- [ ] Update `docs/workflow-contract.md` so the human-readable rules explicitly say the JSON contract is the machine-readable source of truth.
- [ ] Update `skills/evidence-to-ppt-workflow/SKILL.md` and both READMEs to point to the same contract instead of restating divergent hard gates in multiple places.

## Phase 2: Add Validator

- [ ] Add `/Users/sunjieqiong/Documents/Codex/2026-06-26/qin/evidence-to-ppt-workflow/scripts/validate_workflow_pack.py`.
- [ ] Use Python standard library only: `argparse`, `csv`, `json`, `re`, `pathlib`, `sys`.
- [ ] CLI contract:

```bash
python3 scripts/validate_workflow_pack.py examples/complete-run
```

- [ ] Expected pass output:

```text
PASS workflow pack validation
Checked required files: 7
Credible A/B sources: 5
Claims requiring evidence: 6
Slides with source bindings: 5
```

- [ ] Expected failure output must be actionable:

```text
FAIL workflow pack validation
- 03_claims_matrix.md: Claim 2 has status "accepted" but empty Evidence.
- 04_ppt_outline.md: Slide 3 references unknown source id S9.
```

- [ ] Implement checks:
  - required files exist
  - `02_source_table.csv` headers exactly match the contract
  - source IDs are unique and non-empty
  - A/B tier source count is at least `minimum_credible_sources`
  - every accepted or needs-caveat claim has non-empty `Evidence`
  - every evidence source ID in claims exists in `02_source_table.csv`
  - every slide in `04_ppt_outline.md` has `Evidence source_ids:` with at least one known source ID
  - `06_ppt_master_input.md` contains the no-new-claims instruction in English or Chinese
  - no obvious secret-looking values are present in `.md`, `.csv`, `.env.example`, or config files

- [ ] Use non-zero exits:
  - `0` for pass
  - `1` for validation failures
  - `2` for usage, missing contract, or unreadable input path

## Phase 3: Add Validator Tests

- [ ] Add `/Users/sunjieqiong/Documents/Codex/2026-06-26/qin/evidence-to-ppt-workflow/tests/test_validate_workflow_pack.py`.
- [ ] Add fixtures:
  - `tests/fixtures/valid_pack/`
  - `tests/fixtures/invalid_missing_evidence/`
  - `tests/fixtures/invalid_unknown_source/`
  - `tests/fixtures/invalid_low_source_count/`
- [ ] Test cases:

```bash
python3 -m unittest discover -s tests
```

- [ ] Expected local pass:

```text
Ran 4 tests
OK
```

## Phase 4: Add A Complete Passing Example

- [ ] Add `/Users/sunjieqiong/Documents/Codex/2026-06-26/qin/evidence-to-ppt-workflow/examples/complete-run/`.
- [ ] Include all required workflow output files:
  - `00_brief.md`
  - `01_research_pack.md`
  - `02_source_table.csv`
  - `03_claims_matrix.md`
  - `04_ppt_outline.md`
  - `05_audit_report.md`
  - `06_ppt_master_input.md`
- [ ] Use a small public topic that avoids private data and paid API needs, such as `Evidence-first AI slide workflow`.
- [ ] Include at least 5 A/B tier public sources. During implementation, verify the URLs are real before committing. Candidate categories:
  - GPT Researcher repository or documentation
  - ppt-master repository documentation
  - NIST AI Risk Management Framework
  - Stanford HAI AI Index
  - OECD AI Principles or another official AI governance source
- [ ] Add `/Users/sunjieqiong/Documents/Codex/2026-06-26/qin/evidence-to-ppt-workflow/examples/README.md`.
- [ ] Mark existing `examples/example-*.md` and `examples/example-source-table.csv` as format-only examples.
- [ ] Make `examples/complete-run/` the only example that is expected to pass validator hard gates.

## Phase 5: Add CI

- [ ] Add `/Users/sunjieqiong/Documents/Codex/2026-06-26/qin/evidence-to-ppt-workflow/.github/workflows/validate.yml`.
- [ ] CI should run on push and pull request.
- [ ] CI jobs:

```yaml
name: Validate Workflow Pack

on:
  push:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - run: python3 -m unittest discover -s tests
      - run: python3 scripts/validate_workflow_pack.py examples/complete-run
```

- [ ] Add a CI badge to `README.md` and `README.en.md` after the workflow file exists.

## Phase 6: Add Install Acceptance And Dry-Run Guidance

- [ ] Add `/Users/sunjieqiong/Documents/Codex/2026-06-26/qin/evidence-to-ppt-workflow/scripts/smoke_install.py`.
- [ ] This script should not call Codex internals or paid APIs. It should check filesystem presence only.
- [ ] Inputs:

```bash
python3 scripts/smoke_install.py --codex-home ~/.codex
```

- [ ] Checks:
  - `~/.codex/skills/evidence-to-ppt-workflow/SKILL.md` exists
  - `~/.codex/skills/gpt-researcher/SKILL.md` exists
  - `~/.codex/skills/ppt-master/SKILL.md` exists
  - `.env` is not required for dry-run install acceptance
- [ ] Add `/Users/sunjieqiong/Documents/Codex/2026-06-26/qin/evidence-to-ppt-workflow/docs/install-acceptance.md`.
- [ ] Add a dry-run prompt that proves the workflow can start without keys:

```text
用 evidence-to-ppt-workflow 处理这个任务：
主题：Evidence-first AI slide workflow
先不要调用 GPT Researcher，只生成 Phase 0 brief，并列出进入 Phase 1 前需要我确认的 API key 和 provider 配置。
```

- [ ] Document expected dry-run result:
  - Codex should create or propose `00_brief.md`
  - Codex should ask for GPT Researcher provider/search/embedding config before Phase 1
  - Codex should not write any API key unless the user approves the target file

## Phase 7: Update Documentation Without Expanding Scope

- [ ] Update `README.md`:
  - keep Chinese default language selector
  - clarify that the workflow accepts topic-only and document-backed inputs
  - add validator command to Quick Start
  - add complete example path
  - remove completed English README Roadmap item
  - add CI badge after workflow exists
- [ ] Update `README.en.md` with the same operational changes.
- [ ] Update `docs/usage.md` to include the validator command after Phase 4.
- [ ] Update `docs/api-key-setup.md` only if install acceptance mentions `.env`.
- [ ] Update `CHANGELOG.md` under an unreleased section.
- [ ] Update `NOTICE.md` only if added files change third-party project references.

## Phase 8: Add Issue Templates And Release Path

- [ ] Add `.github/ISSUE_TEMPLATE/bug_report.yml`.
- [ ] Add `.github/ISSUE_TEMPLATE/validation_failure.yml`.
- [ ] Add `.github/ISSUE_TEMPLATE/feature_request.yml`.
- [ ] Add `.github/ISSUE_TEMPLATE/config.yml`.
- [ ] Add `/Users/sunjieqiong/Documents/Codex/2026-06-26/qin/evidence-to-ppt-workflow/docs/release.md`.
- [ ] Release path after validation passes:

```bash
git status --short
python3 -m unittest discover -s tests
python3 scripts/validate_workflow_pack.py examples/complete-run
git diff --check
git tag -a v0.1.0 -m "v0.1.0"
git push origin main
git push origin v0.1.0
```

Do not create or push a tag until the user explicitly approves release tagging.

## Implementation Order

- [ ] Contract files first, because validator and docs depend on them.
- [ ] Validator second, with a minimal failing/pass fixture set.
- [ ] Complete example third, then make validator pass on it.
- [ ] CI fourth, using the exact local commands.
- [ ] Install acceptance fifth.
- [ ] Documentation and issue templates last.

## Local Verification Before Commit

Run from `/Users/sunjieqiong/Documents/Codex/2026-06-26/qin/evidence-to-ppt-workflow`:

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_workflow_pack.py examples/complete-run
python3 scripts/smoke_install.py --codex-home ~/.codex
git diff --check
git status --short
```

If `smoke_install.py` fails because the local machine does not have all three skills installed, keep the failure message actionable and do not block repository CI on local skill presence.

## Acceptance Criteria

- [ ] CI exists and passes locally equivalent commands.
- [ ] `examples/complete-run/` passes validator.
- [ ] At least one intentionally invalid fixture fails with a clear error.
- [ ] Existing format-only examples no longer imply they satisfy the 5-source gate.
- [ ] README, README.en, SKILL.md, and docs/workflow-contract.md point to the same machine-readable contract.
- [ ] No real API key, bearer token, or private credential appears in the repository.
- [ ] GitHub issue templates exist.
- [ ] Roadmap no longer lists completed bilingual README work as pending.

## Commit Plan

- [ ] `feat: add workflow pack contract and validator`
- [ ] `test: add validator fixtures and complete example`
- [ ] `ci: validate workflow packs in GitHub Actions`
- [ ] `docs: document validation and install acceptance`
- [ ] `chore: add issue templates and release notes`

## Risks And Mitigations

- Validator parsing Markdown can be brittle. Keep required labels simple and documented: `Status:`, `Evidence:`, and `Evidence source_ids:`.
- Public source examples may drift. Choose stable official or repository URLs, and keep exact claims modest.
- CI cannot verify a user's local Codex installation. Keep install acceptance as an optional local smoke test, not a CI gate.
- Rule drift can return if docs restate every gate. Keep detailed hard gates in `workflow/contract.json` and have docs summarize them.
