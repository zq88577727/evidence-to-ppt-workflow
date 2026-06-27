# Security

## Secret Handling

Never commit:

- API keys
- `.env`
- access tokens
- customer source documents
- private generated research packs
- final PPT deliverables with confidential content

Use `.env.example` as a template only.

## Reporting Security Issues

Open a private GitHub security advisory if available, or contact the repository
owner directly. Do not disclose active secrets in public issues.

## Workflow Safety

This workflow may call external services through GPT Researcher, retrievers,
LLM providers, or embedding providers. Review each provider's data handling
terms before sending sensitive content.

Codex should not save API keys unless the user explicitly approves a target
file or environment.
