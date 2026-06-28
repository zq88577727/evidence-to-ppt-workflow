# Workflow Contract

The machine-readable source of truth is
[`workflow/contract.json`](../workflow/contract.json). This document explains
the same gates for humans. If a rule drifts, update the JSON contract first and
then update this file, `README.md`, `README.en.md`, and
`skills/evidence-to-ppt-workflow/SKILL.md`.

## Phase 0: Brief

Create `00_brief.md` with topic, audience, scope, deck length, geography,
time window, source policy, exclusions, language, assumptions, and any supplied
source materials such as PDFs, reports, URLs, outlines, or Markdown files.

## Phase 1: Research Pack

Use GPT Researcher when configured. Output `01_research_pack.md`.

Required research behavior:

- facts include URLs or DOI-like identifiers
- no unsupported statistics
- separate facts, estimates, and analysis
- include publication or access dates when available
- keep source diversity appropriate to the topic

## Phase 2: Source Audit

Create:

- `02_source_table.csv`
- `03_claims_matrix.md`
- `05_audit_report.md`

No claim may enter the deck without at least one accepted source.

Reliability tiers:

- A: official, government, regulator, filing, peer-reviewed paper, standards body
- B: established research institution, reputable industry report, major media with clear sourcing
- C: blog, vendor marketing, social/community source, unsourced secondary commentary
- Reject: inaccessible, irrelevant, circular, AI-generated, or unable to support the claim

## Phase 3: PPT Outline

Create `04_ppt_outline.md` only after the audit passes.

Each slide must include title, message, evidence source IDs, visual idea,
speaker note, and footnote text.

## Phase 4: ppt-master Input

Create `06_ppt_master_input.md` as the single source file for ppt-master.

It must instruct ppt-master not to introduce factual claims outside the approved
materials.

## Stop Conditions

Stop and report the blocker if:

- fewer than 5 credible sources remain
- the central claim is unsupported
- API keys are missing
- required companion skills are missing
- upstream commands fail

## Local Validation

Validate a completed material pack with:

```bash
python3 scripts/validate_workflow_pack.py path/to/workflow-pack
```

The validator checks the required files, source table headers, A/B source count,
claim evidence bindings, slide source bindings, and the no-new-claims constraint
in `06_ppt_master_input.md`.

## Delivery Criteria

A completed workflow run should have:

- enough A/B-tier sources to support the deck's central message
- no accepted deck claim without a source id
- caveats for directional or weakly supported claims
- a `06_ppt_master_input.md` file that tells ppt-master not to add new factual claims
- an editable PPTX from ppt-master when the user requested the final deck, or a clear blocked reason
