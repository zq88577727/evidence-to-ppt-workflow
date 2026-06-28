# Design Notes

This workflow is intentionally small. It is a local Codex orchestration layer, not a replacement for GPT Researcher, ppt-master, or human source review.

## Why The Workflow Has Gates

The project separates research, source audit, claims matrix, outline, and PPT generation because each stage has a different failure mode:

- Research can find useful sources but still mix facts, estimates, and interpretation.
- Source audit can reject weak sources before claims reach a deck.
- Claims matrix review keeps each slide-worthy claim tied to source IDs and caveats.
- ppt-master receives a constrained input file so it can focus on slide generation without adding new facts.

## Why Validation Is Local And Deterministic

The validator does not call model providers or search APIs. It checks structural requirements that should be true for every reusable material pack:

- required workflow files exist
- source table headers match the contract
- at least five A/B-tier sources remain
- accepted and caveated claims include parseable source IDs
- every outline slide references known source IDs
- ppt-master input contains the no-new-claims constraint

This keeps CI cheap, deterministic, and safe for public contributors.

## What Validation Does Not Prove

The validator does not prove that every cited source is factually correct, current, or sufficient for a user's domain. It confirms traceability and workflow contract compliance. Human review is still required for high-stakes or externally published decks.

## Public Example Policy

`examples/complete-run/` is a small public fixture. It demonstrates a passing workflow pack without paid APIs or private data. The older `examples/example-*` files are format examples only and are not treated as delivery-grade packs.
