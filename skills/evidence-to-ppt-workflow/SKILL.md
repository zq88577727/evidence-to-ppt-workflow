---
name: evidence-to-ppt-workflow
description: Use when the user wants a source-backed PPT workflow from a topic, idea, PDF, report, outline, URL, or Markdown source, with a research pack, claims matrix, Codex source review, and ppt-master handoff.
---

# Evidence To PPT Workflow

## Purpose

Turn a topic or existing source material into a presentation through three gated phases:

1. `gpt-researcher` gathers sources and drafts a research pack.
2. Codex audits sources and builds a claims matrix.
3. `ppt-master` converts approved material into a PPT.

Do not skip the audit gate. The workflow is designed for traceable evidence, not generic web summaries.

Hard delivery gates are defined in this skill package's `workflow/contract.json`.
Use that machine-readable contract for validator-compatible file names,
source-table headers, minimum credible source count, claim evidence requirements,
slide source bindings, and ppt-master handoff constraints.

## Trigger

Use this skill when the user asks for any of these:

- start from only a topic, idea, thesis, or question
- start from a PDF, report, webpage, outline, Markdown file, or mixed source material that still needs evidence review
- generate PPT support material before making slides
- make a presentation with verifiable sources
- research first, then create a deck
- "主题 -> 证据材料包 -> PPT"

If the user already supplied a clean source document and only wants slides with no extra research, audit, source table, or claims matrix, use `ppt-master` directly.

## Required Companion Skills

Before running each phase, read the relevant companion skill:

- Phase 1: read `gpt-researcher/SKILL.md`.
- Phase 3: read `ppt-master/SKILL.md`.

Resolve companion skills from installed Codex skill roots, normally:

- `~/.codex/skills/gpt-researcher/SKILL.md`
- `~/.codex/skills/ppt-master/SKILL.md`

If either skill is missing, report the missing dependency and continue with the best available fallback only after telling the user.

## Output Location

Create a project folder under the current workspace:

```text
work/evidence-to-ppt/<topic-slug>/
  00_brief.md
  01_research_pack.md
  02_source_table.csv
  03_claims_matrix.md
  04_ppt_outline.md
  05_audit_report.md
  06_ppt_master_input.md
  ppt-master-project/        # created later by ppt-master, if applicable
```

Use stable file names so future turns can resume without re-deriving state.

## Phase 0: Scope The Topic

If the user gives only a topic, infer sensible defaults and write `00_brief.md`.
If the user supplies PDFs, reports, URLs, outlines, or Markdown files, summarize the provided materials in `00_brief.md` and treat them as initial sources for Phase 1 and Phase 2.
Ask a question only when the answer materially changes research boundaries.

`00_brief.md` must include:

- topic
- audience
- intended deck length
- geography and time window
- source preference: official, academic, financial filing, standards, government, reputable industry reports
- excluded source types
- output language
- known assumptions
- supplied source materials, if any

Default deck length: 8-12 slides.
Default source policy: prefer primary and authoritative sources; blogs and social posts are background only.

## Phase 1: GPT Researcher Evidence Gathering

Read `gpt-researcher/SKILL.md` first.

Use GPT Researcher to produce `01_research_pack.md`. If API keys or local configuration are missing, stop and ask the user for the required key or target config path. Never persist API keys unless the user explicitly tells you where to store them.

Recommended GPT Researcher settings for cost control:

```env
REPORT_SOURCE=web
REPORT_FORMAT=APA
MAX_ITERATIONS=3
MAX_SEARCH_RESULTS_PER_QUERY=5
TOTAL_WORDS=1800
CURATE_SOURCES=True
```

The research prompt must require:

- factual claims with URLs or DOI-like identifiers
- publication date or retrieval date when available
- distinction between facts, estimates, and analysis
- no unsupported statistics
- no invented source titles
- enough source diversity for the topic

If GPT Researcher cannot be run in the current environment, use available web/search tools manually and state that Phase 1 was performed without GPT Researcher automation.

## Phase 2: Codex Source Audit

Codex must turn the research pack into three files:

### `02_source_table.csv`

Columns:

```text
source_id,title,author_or_org,date,url,source_type,access_date,claim_supported,quoted_or_paraphrased_evidence,reliability_tier,notes
```

Reliability tiers:

- `A`: official/government/regulator/company filing/peer-reviewed paper/standards body
- `B`: established research institution, reputable industry report, major media with clear sourcing
- `C`: blog, vendor marketing, social/community source, unsourced secondary commentary
- `Reject`: inaccessible, irrelevant, circular, AI-generated, or cannot support the claim

### `03_claims_matrix.md`

Every slide-worthy claim must include:

```text
Claim:
Status: accepted | needs caveat | rejected
Evidence: source_id list
Reasoning:
Deck wording:
Risk/caveat:
```

Rules:

- No claim enters the deck without at least one accepted source.
- Quantitative claims need a date, scope, and denominator when applicable.
- Keep source statements separate from Codex interpretation.
- If two reliable sources conflict, preserve the disagreement instead of averaging silently.
- Reject claims supported only by weak or circular sources.

### `05_audit_report.md`

Include:

- accepted source count
- rejected source count
- highest-risk claims
- missing evidence
- whether the material is ready for PPT

Hard gate: if fewer than 5 credible sources remain, or the central claim lacks evidence, stop and ask whether to broaden the research.

For reusable packs, run the packaged validator when available:

```bash
python3 ~/.codex/skills/evidence-to-ppt-workflow/scripts/validate_workflow_pack.py work/evidence-to-ppt/<topic-slug>
```

## Phase 3: PPT Outline

Write `04_ppt_outline.md` only after the audit gate passes.

Each slide entry must include:

```text
Slide:
Title:
Message:
Evidence source_ids:
Visual idea:
Speaker note:
Footnote text:
```

Default outline:

1. Context and question
2. Current state
3. Evidence-backed trend or problem
4. Key drivers
5. Counterpoint or limitation
6. Case/example
7. Implications
8. Recommended action or conclusion
9. Appendix/source notes if needed

Adapt the structure to the topic, but keep every slide tied to evidence.

## Phase 4: PPT Master Input

Read `ppt-master/SKILL.md` before starting this phase.

Write `06_ppt_master_input.md` as the single source document for `ppt-master`. It must include:

- approved slide outline
- approved claims matrix summary
- source table excerpt
- footnote requirements
- style brief if supplied by the user
- explicit instruction: do not introduce new factual claims not present in the approved materials

Then invoke `ppt-master` using `06_ppt_master_input.md` as source content. Follow all blocking gates and serial execution rules from `ppt-master`.

## Completion Contract

Do not call the workflow complete until these exist:

- `00_brief.md`
- `01_research_pack.md`
- `02_source_table.csv`
- `03_claims_matrix.md`
- `04_ppt_outline.md`
- `05_audit_report.md`
- `06_ppt_master_input.md`

If the user asked for the final PPT, also require the final `ppt-master` output or a clear blocked reason.

## Common Mistakes

- Letting GPT Researcher output go straight into slides without source review.
- Treating a citation list as proof that each claim is supported.
- Mixing facts and Codex interpretation in the same sentence.
- Using low-quality blogs as evidence for quantitative claims.
- Starting `ppt-master` before the claims matrix is accepted.
- Saving API keys into files without an explicit user-approved target.
