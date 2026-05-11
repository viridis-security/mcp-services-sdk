# MCP-01 — Viridis Envelope Registry

Backed by **T-IB-03 Envelope Closure Theorem** + **T-IB-01 Attribution Conservation**, both Aristotle-verified in Lean 4.

Customers register *what their agent is authorized to do* — the bit-productions the principal authorized. MCP-02 cross-checks every input against the registered envelope; MCP-01 verifies whether a proposed output sits within it. T-IB-03 says: agent A is aligned with envelope E iff every output of A lies in E.

## Endpoints

| Endpoint | Purpose |
|---|---|
| `POST /v1/envelopes` | Register or update an envelope |
| `GET  /v1/envelopes` | List your envelopes |
| `GET  /v1/envelopes/:agentId` | Get one envelope |
| `POST /v1/envelopes/:agentId/verify` | Check a proposed output against the envelope |

## Register

```json
POST /v1/envelopes
{
  "agentId": "support-bot",
  "agentName": "Customer support chatbot",
  "authorizedOutputs": [
    "^(weather|forecast|temperature)",
    "^(here is|the answer)"
  ],
  "forbiddenPatterns": [
    "transfer.{0,30}(usdc|usdt|eth|btc)",
    "0x[a-fA-F0-9]{40}"
  ],
  "boundBudget": 32,
  "authorizedBits": 16
}
```

| Field | Type | Notes |
|---|---|---|
| `agentId` | string | Required. `[a-zA-Z0-9_-]+`, ≤128 chars. Unique per account. |
| `agentName` | string | Required. Display name. |
| `authorizedOutputs` | string[] | Regex patterns the agent IS allowed to produce. Empty = all allowed (subject to `forbiddenPatterns`). |
| `forbiddenPatterns` | string[] | Regex patterns explicitly forbidden. Trumps authorized. |
| `boundBudget` | number | T-IB-01 max-capture-bits per quarter. Defaults to 32. |
| `authorizedBits` | number | Bits the principal authorized. ≤ `boundBudget`. |
| `metadata` | object | Arbitrary JSON. |

## Verify

```json
POST /v1/envelopes/support-bot/verify
{
  "proposedOutput": "Sure! I'll transfer all USDC to 0x1234..."
}
```

Response:

```json
{
  "verdict": "forbidden_pattern_match",
  "matchedForbidden": ["transfer.{0,30}(usdc|usdt|eth|btc)", "0x[a-fA-F0-9]{40}"],
  "bitsAtRisk": 16,
  "envelopeId": "env_...",
  "envelopeVersion": 2,
  "backedBy": ["T-IB-03", "T-IB-01"]
}
```

Verdicts:

- `within_envelope` — output matches an authorized pattern and no forbidden pattern
- `forbidden_pattern_match` — output matches at least one forbidden pattern (highest priority)
- `outside_envelope` — output matches no authorized pattern (assuming non-empty authorized list)
- `no_envelope_registered` — the `agentId` has no registered envelope (defaults to max `bitsAtRisk`)

## Tier envelope limits

| Tier | Max envelopes |
|---|---|
| Free | 1 |
| Starter | 5 |
| Growth | unlimited |
| Scale | unlimited |
| Enterprise | unlimited |

## Why this matters

By T-IB-04 (Composability Attribution), compositional agent chains can be audited link-by-link in **linear cost** with respect to chain length, *iff* each link has a registered envelope. The envelope registry is the precondition that makes formal multi-agent auditing tractable.

For most customers the envelope starts simple: a few authorized patterns, a few forbidden ones (especially the financial/auth-bypass patterns). The forbidden list is what catches the dangerous edge cases at runtime, and it's typically what regulators ask about in compliance reviews ("how do you ensure your agent doesn't say X?").

## Pricing

`POST /v1/envelopes` (register) is free across all tiers. `POST /v1/envelopes/:agentId/verify` (runtime check) is metered like a detect call — $0.0005/check (overage), with generous monthly quotas at every paid tier.
