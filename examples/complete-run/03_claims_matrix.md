# Claims Matrix

## Claim 1

Claim: A source-backed PPT workflow should separate evidence gathering, source audit, claims matrix creation, and slide generation.
Status: accepted
Evidence: S1, S2, S3
Reasoning: GPT Researcher and ppt-master support distinct tool roles; NIST supports documented risk management practices. The workflow adds an audit gate between research and slide generation.
Deck wording: "Use a gated flow: research first, audit every claim, then generate slides from approved material."
Risk/caveat: This is a workflow design claim, not proof that all output will be correct.

## Claim 2

Claim: GPT Researcher is suitable as the research-pack layer when configured with a model provider and retriever.
Status: accepted
Evidence: S1
Reasoning: The public repository describes GPT Researcher as an autonomous research agent that produces cited reports.
Deck wording: "GPT Researcher prepares the first evidence pack, but the pack still needs review."
Risk/caveat: Runtime quality depends on provider configuration, search coverage, and source review.

## Claim 3

Claim: ppt-master should receive only reviewed material when the user needs traceable PPT content.
Status: accepted
Evidence: S2, S3
Reasoning: ppt-master covers the generation layer, while NIST supports using documented controls for AI workflows.
Deck wording: "ppt-master starts after the claims matrix is accepted."
Risk/caveat: This does not evaluate ppt-master visual quality or conversion fidelity.

## Claim 4

Claim: Broad AI reports are useful context but should not be treated as narrow market statistics without additional evidence.
Status: needs caveat
Evidence: S4, S3
Reasoning: Stanford HAI provides broad AI context, and NIST supports careful risk-aware handling of AI-related claims.
Deck wording: "Use broad AI signals as context; verify topic-specific numbers before they enter slides."
Risk/caveat: Do not convert broad AI trends into SMB, industry, or country-specific numbers without direct sources.

## Claim 5

Claim: The workflow should make source traceability visible through a source table and claims matrix.
Status: accepted
Evidence: S3, S5
Reasoning: NIST and OECD support transparent, accountable handling of AI-related workflows. A source table and claims matrix make the evidence trail explicit.
Deck wording: "Every slide-worthy claim carries source IDs and caveats."
Risk/caveat: Traceability helps review, but it does not replace expert judgment.

## Claim 6

Claim: This repository is an orchestration layer, not an official plugin from the referenced projects.
Status: accepted
Evidence: S1, S2
Reasoning: The workflow references GPT Researcher and ppt-master as dependencies, but it is maintained separately.
Deck wording: "This workflow coordinates existing tools; it does not replace their official documentation."
Risk/caveat: Users should follow upstream project configuration for model, retriever, and PPT generation details.
