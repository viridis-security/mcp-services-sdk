# @viridis/mcp-client (TypeScript)

**Apache-2.0 — Open Source.** Client SDK for Viridis MCP services.

```bash
npm install @viridis/mcp-client
```

```typescript
import { ViridisMCP } from "@viridis/mcp-client";

const viridis = new ViridisMCP({ apiKey: process.env.VIRIDIS_API_KEY! });

const result = await viridis.injection.detect({
  input: untrustedUserMessage,
  certainty: "standard",
});

if (result.recommendedAction === "reject") {
  throw new Error(`Injection detected: p=${result.probability}, bits at risk=${result.bitsAtRisk}`);
}
```

Get an API key at https://mcp.viridis-security.com. Free tier: 1,000 calls/mo.

This SDK is open source (Apache 2.0). The hosted MCP server it talks to is proprietary; backing theorems are formally verified — see https://github.com/viridis-security/corpus.
