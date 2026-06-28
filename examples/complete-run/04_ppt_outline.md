# PPT Outline

## Slide 1

Title: 从主题到有证据的 PPT
Message: 不直接从想法跳到 PPT，而是先生成可审查的证据材料包。
Evidence source_ids: S1, S2, S3
Visual idea: Topic -> Research Pack -> Source Audit -> Claims Matrix -> PPT.
Speaker note: 说明这个流程解决的是 traceability，而不是承诺模型永远正确。
Footnote text: Sources: GPT Researcher; ppt-master; NIST AI RMF.

## Slide 2

Title: 三个角色，各做一件事
Message: GPT Researcher 找证据，Codex 审证据，ppt-master 做页面。
Evidence source_ids: S1, S2
Visual idea: Three columns for research, audit, and production.
Speaker note: 强调 GPT Researcher 的输出不能直接进入 slides。
Footnote text: Sources: GPT Researcher repository; ppt-master repository.

## Slide 3

Title: 审查门槛前置
Message: 每个进入 PPT 的 claim 都要先经过 source table 和 claims matrix。
Evidence source_ids: S3, S5
Visual idea: Gate diagram with accepted, needs caveat, rejected.
Speaker note: 解释 source id、status、caveat 三个字段。
Footnote text: Sources: NIST AI RMF; OECD AI Principles.

## Slide 4

Title: 背景材料不能自动变成结论
Message: 行业报告可以做背景，但窄口径结论需要直接证据。
Evidence source_ids: S4, S3
Visual idea: Funnel from broad context to specific claim.
Speaker note: 用 broad AI trend 与 specific market statistic 的区别说明风险。
Footnote text: Sources: Stanford HAI AI Index; NIST AI RMF.

## Slide 5

Title: 交给 ppt-master 前冻结事实边界
Message: `06_ppt_master_input.md` 必须明确不能新增未经审查事实。
Evidence source_ids: S2, S3
Visual idea: Locked handoff document feeding slide generation.
Speaker note: 生成层可以改表达和视觉，不应新增事实。
Footnote text: Sources: ppt-master repository; NIST AI RMF.
