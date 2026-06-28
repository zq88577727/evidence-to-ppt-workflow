# Research Pack

## Research Question

How should a local Codex workflow turn a broad presentation topic into a source-backed PPT input package without letting unsupported claims enter the final deck?

## Evidence Summary

GPT Researcher is used as the research layer because its public project documentation describes an autonomous research agent that produces reports with citations. This supports the role of evidence gathering, but it does not by itself prove that every generated claim is correct.

ppt-master is used as the presentation production layer because its public repository describes AI-driven SVG/PPT generation from source material. This supports the final handoff layer, but the workflow should prevent ppt-master from adding new factual claims that were not reviewed.

NIST AI RMF supports the idea that AI-related workflows benefit from documented risk management and review practices. It is a governance source, not a PPT-generation source.

Stanford HAI AI Index provides broad public context on AI progress and adoption. It is useful for background framing, but broad AI context should not be converted into narrow market statistics without topic-specific evidence.

OECD AI Principles provide an intergovernmental framing for trustworthy AI. They support the use of transparency and accountability language in the workflow's quality gates.

## Interpretation

The safest deck-production path is not "topic directly to PPT". It is "topic or source material to research pack, then source audit, then claims matrix, then PPT outline, then ppt-master input". The source audit and claims matrix are the critical control points.

## Limitations

This example does not verify GPT Researcher runtime behavior or ppt-master output quality. It validates a workflow contract and sample material pack.
