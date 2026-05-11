# Integration recipes

Drop-in patterns for the major agent frameworks. All examples use the open-source `@viridis/mcp-client` (TypeScript) or `viridis-mcp-client` (Python) SDK.

| Framework | Recipe |
|---|---|
| LangChain (Python + JS) | [langchain.md](langchain.md) |
| Microsoft AutoGen | [autogen.md](autogen.md) |
| OpenAI Agents SDK / Assistants API | [openai-agents.md](openai-agents.md) |
| Crew AI | _coming next_ |
| Mastra | _coming next_ |
| Custom agent loop | see [examples/](../../examples) |

## Common pattern

Every recipe follows the same three-step shape:

1. **Pre-message gate** — run `viridis.injection.detect` on every untrusted input *before* it reaches the LLM
2. **Action recommendation** — `allow` / `sanitize` / `reject` / `escalate`
3. **(Optional) Maxwell challenge** — when verdict is `suspicious`, return a proof-of-work challenge instead of immediately rejecting

This pattern is formally compositional. See **T-IB-04 Composability Attribution Theorem** (Aristotle-verified): chain audits decompose link-by-link with linear cost in chain length.

## Contributing

Have a recipe for a framework not listed? Open a PR — examples that show real working code (not just pseudocode) are very welcome.
