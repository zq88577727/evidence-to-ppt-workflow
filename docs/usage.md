# Usage

## Install

```bash
mkdir -p ~/.codex/skills
cp -R skills/evidence-to-ppt-workflow ~/.codex/skills/evidence-to-ppt-workflow
```

Restart Codex after installing the skill.

## Basic Prompt

```text
用 evidence-to-ppt-workflow 做这个主题：AI Agent 在中小企业的落地情况。
目标听众是中小企业老板，10 页以内，需要中文 PPT，所有关键判断都要有来源。
```

## Stop Before PPT

```text
用 evidence-to-ppt-workflow 生成“生成式 AI 对咨询行业交付模式的影响”的证据材料包和 PPT 大纲。先不要生成最终 PPT。
```

## Start From Existing Materials

```text
用 evidence-to-ppt-workflow 基于这份 PDF 和我已有的大纲生成 PPT 材料包。
请先补充外部权威来源，审查每个关键观点，再整理 claims matrix 和 ppt-master 输入文件。
```

Use `ppt-master` directly only when the supplied material is already complete,
trusted, and ready for slides without additional research or source audit.

## Expected Outputs

```text
work/evidence-to-ppt/<topic-slug>/
  00_brief.md
  01_research_pack.md
  02_source_table.csv
  03_claims_matrix.md
  04_ppt_outline.md
  05_audit_report.md
  06_ppt_master_input.md
```

## Gate Behavior

The workflow should stop before creating slides if:

- fewer than 5 credible sources remain after audit
- the central claim lacks evidence
- API keys are missing for Phase 1
- GPT Researcher or ppt-master is not installed
- the user asks to stop after the materials pack
