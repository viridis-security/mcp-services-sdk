# MCP-02: Adversarial Injection Detector

**Tier 1 / MVP (target: ship 30 days)**
**Backed by:** T-IB-02 (Adversarial Landauer Inequality), T-IB-06 (Detection Lower Bound)

Detects adversarial-attribution-break attempts in untrusted input. Customer agents pipe input through this MCP before consumption; we return a probability of injection + bits-at-risk + recommended action.

## API

### Tool: `injection.detect`

**Request:**
```json
{
  "input": "string (the untrusted text/data)",
  "context": "string (optional: the agent's role/system prompt; helps the detector calibrate)",
  "certainty": "quick | standard | premium",
  "agentId": "string (optional: for envelope cross-check if MCP-01 also subscribed)"
}
```

**Response:**
```json
{
  "verdict": "clean | suspicious | attack",
  "probability": 0.0,
  "bitsAtRisk": 0,
  "operatingPoint": { "alpha": 0.001, "beta": 0.001 },
  "matchedPatterns": ["VC-AI-PROMPT-0001", "..."],
  "recommendedAction": "allow | sanitize | reject | escalate",
  "explainabilityToken": "<id for retrieving full reasoning>",
  "billing": { "cost": 0.001, "tier": "starter", "remaining": 49872 }
}
```

The `bitsAtRisk` field exposes the corpus theorem's output directly — it's the upper bound on adversarial capture if the input is consumed unchecked, computed per T-IB-02 + T-IB-01.

### Tool: `injection.explain`

Given an `explainabilityToken` from a previous `detect` call, returns the detector's reasoning trace. Used for audit logs and incident review.

## Pricing

Per the Tier table in `MCP_MICROSERVICES_STRATEGY.md` §4.1:
- Free: 1,000 calls/mo
- Starter ($49/mo): 50K calls/mo
- Growth ($299/mo): 500K calls/mo
- Scale ($1,499/mo): 5M calls/mo
- Enterprise: custom
- Overage: $0.001/call (auto-graduates if sustained)

## Implementation

The server in `src/` is **closed-source** (proprietary moat per `MCP_MICROSERVICES_STRATEGY.md` §10). It wraps the existing `viridis_engine` injection-detection codepath, adds MCP protocol, auth, rate limiting, billing.

The SDK in `mcp-services/sdk/typescript` is **open-source** (Apache 2.0).

## Hosting

DigitalOcean App Platform. Spec at `deploy/app.yaml`.
Production endpoint: `https://mcp.viridis-security.com/v1/injection`

## Status

- [x] Scaffold structure
- [ ] Server implementation (wraps `viridis_engine`)
- [ ] Auth layer (API key in header)
- [ ] Rate limiter (Redis token bucket)
- [ ] Billing hook (Stripe metered)
- [ ] DO App Platform deployment
- [ ] SDK published (`@viridis/mcp-client`)
- [ ] Integration examples
- [ ] First design partner onboarded
