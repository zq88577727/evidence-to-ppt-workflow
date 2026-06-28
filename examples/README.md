# Examples

This directory contains two kinds of examples:

- `example-*` files are compact format examples. They show file shapes and field names, but they are not intended to satisfy every delivery gate.
- `complete-run/` is the validator-passing example. Use it when checking the workflow contract or CI.

Run:

```bash
python3 scripts/validate_workflow_pack.py examples/complete-run
```

The complete example is intentionally small and public. It demonstrates evidence traceability without calling GPT Researcher, ppt-master, or paid APIs.
