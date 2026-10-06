# @viridis/mcp-client (TypeScript)

**Apache-2.0 — Open Source.** Client SDK for Viridis MCP services.

## Install and build from source

As checked on October 6, 2026, `@viridis/mcp-client` has no public npm release. Build the public source and record the checkout commit instead. Use Git, Node.js 20, 22, or 24+ (a version supported by the development toolchain), and npm. The local verification uses Node.js 20.20.2. Dependency installation requires access to npm; the import check itself needs no API key or hosted service.

```bash
git clone https://github.com/viridis-security/mcp-services-sdk.git
cd mcp-services-sdk
# This repair is under review in PR #8; default main is not yet corrected.
git fetch origin pull/8/head
git checkout --detach FETCH_HEAD
git rev-parse HEAD
cd sdk/typescript
npm ci --ignore-scripts
npm run build
npm test
node --input-type=module -e 'import { ViridisMCP } from "./dist/index.js"; console.log(typeof ViridisMCP)'
```

Expected local output: `function`. The SDK's committed npm lockfile fixes the development dependency graph. `npm ci --ignore-scripts` installs that exact graph without dependency lifecycle scripts; run `npm run build` explicitly afterward. The build emits `dist/index.js` and `dist/index.d.ts`, as declared in `package.json`.

To use the built package in your own Node project, run the following **from that project's directory**, replacing the path with your source checkout:

```bash
npm install /absolute/path/to/mcp-services-sdk/sdk/typescript
node --input-type=module -e 'import { ViridisMCP } from "@viridis/mcp-client"; console.log(typeof ViridisMCP)'
```

Build the SDK before installing the local directory. This retains the package-name import used in the example below without relying on an unavailable registry release.

## Hosted usage requires a separate service check

Calling `injection.detect` needs a valid service-issued API key and the proprietary hosted service. The local build/import check sends no request and proves no hosted response, billing, availability, or theorem guarantee. [Draft PR #8](https://github.com/viridis-security/mcp-services-sdk/pull/8) tracks the missing authoritative hosted implementation/contract; its skipped acceptance stubs are not passing hosted tests. Treat the existing example below as client-interface usage, not verified hosted acceptance.

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
