# Contributing

Contributions are welcome when they improve the workflow's reliability, source
traceability, documentation, or safety.

## Good Contributions

- Better source-audit rules.
- Better claims matrix examples.
- More provider configuration examples that follow GPT Researcher conventions.
- Documentation fixes.
- Validation scripts that catch missing sources or accidental secrets.

## Please Avoid

- Adding real API keys or credentials.
- Claiming official affiliation with upstream projects.
- Adding unsupported benchmarks, fake stars, fake users, or unverifiable claims.
- Making the workflow skip the source-audit gate.

## Development Checklist

1. Keep `skills/evidence-to-ppt-workflow/SKILL.md` concise and Codex-readable.
2. Keep README examples public and non-sensitive.
3. Make sure `.env.example` contains only blank placeholder values.
4. Verify examples do not include private customer data.
5. Update `CHANGELOG.md` for user-visible changes.
