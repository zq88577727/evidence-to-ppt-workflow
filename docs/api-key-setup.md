# API Key And Model Setup

This workflow follows GPT Researcher provider configuration. It does not bind
the user to one model vendor.

## When Keys Are Needed

Keys are needed only when Phase 1 starts GPT Researcher evidence gathering.
Phase 0 brief creation does not need API keys.

## Safe Setup

```bash
cp .env.example .env
```

Then edit `.env` locally. Do not commit `.env`.

## LLM Provider

Use one GPT Researcher-supported provider. DeepSeek is only an example profile,
not a requirement of this workflow.

```env
DEEPSEEK_API_KEY=
FAST_LLM=deepseek:deepseek-chat
SMART_LLM=deepseek:deepseek-chat
STRATEGIC_LLM=deepseek:deepseek-chat
```

Alternative providers include OpenAI, Anthropic, Azure OpenAI, Google Gemini,
Groq, Mistral, Ollama, Together, DashScope, OpenRouter, MiniMax, Bedrock,
HuggingFace, LiteLLM, DeepSeek, and others supported by GPT Researcher. Use
the exact provider prefix and model name from GPT Researcher official docs.

## Retriever

```env
RETRIEVER=tavily
TAVILY_API_KEY=
BRAVE_API_KEY=
```

Use Tavily, Brave, or another GPT Researcher-supported retriever.

## Embedding

```env
EMBEDDING=ollama:nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434
```

You can also use OpenAI, Google, Mistral, Cohere, VoyageAI, DashScope,
HuggingFace, or other GPT Researcher-supported embedding providers.

## Codex Rule

Codex should ask before saving secrets and should only write keys to a target
file explicitly approved by the user.
