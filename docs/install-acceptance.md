# Install Acceptance

Use this page after installing the workflow and its companion skills.

## Filesystem Smoke Check

Run from the repository root:

```bash
python3 scripts/smoke_install.py --codex-home ~/.codex
```

Expected pass:

```text
PASS install smoke check
- found evidence-to-ppt-workflow
- found gpt-researcher
- found ppt-master
```

If a skill is missing, install it first and restart Codex.

## Dry-Run Prompt

Use this prompt to verify that the workflow can start without API keys:

```text
用 evidence-to-ppt-workflow 处理这个任务：
主题：Evidence-first AI slide workflow
先不要调用 GPT Researcher，只生成 Phase 0 brief，并列出进入 Phase 1 前需要我确认的 API key 和 provider 配置。
```

Expected behavior:

- Codex should scope or create `00_brief.md`.
- Codex should not call GPT Researcher.
- Codex should ask for model, retriever, and embedding configuration before Phase 1.
- Codex should not write API keys to a file unless the user explicitly approves the target file.

This check validates installation and activation path, not source quality or final PPT output.
