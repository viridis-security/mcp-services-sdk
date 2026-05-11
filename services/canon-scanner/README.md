# MCP-03 — Viridis Canon Scanner

`POST /v1/canon/scan` — submit source code, get back matched canon entries with mitigation pointers and bits-at-risk per match.

Backed by **T-IB-05** (Canon Compression Theorem): expected cost-per-finding for canon-known patterns decays exponentially as the canon grows. Verified by Aristotle (Harmonic).

## Request

```json
{
  "source": "import openai\nopenai.api_key = \"sk_live_...\"\n...",
  "language": "python",
  "certainty": "standard"
}
```

| Field | Type | Notes |
|---|---|---|
| `source` | string | Required. Raw source code to scan, ≤5 MB. |
| `language` | string | Optional. `typescript` \| `python` \| `javascript` \| `go` \| `rust` \| `auto`. Defaults to auto-detect. |
| `certainty` | string | `quick` (α=10⁻²), `standard` (α=10⁻³), `premium` (α=10⁻⁶). |
| `agentId` | string | Optional. Registered envelope ID to cross-check matches against. |

## Response

```json
{
  "matches": [{
    "entryId": "VC-AI-API-0001",
    "category": "Hardcoded API key or secret",
    "severity": "critical",
    "bitsAtRisk": 38,
    "occurrences": [{"line": 2, "snippet": "openai.api_key = \"sk_live_...\""}],
    "mitigation": "Move secrets to environment variables; rotate any leaked credentials immediately.",
    "references": ["https://cwe.mitre.org/data/definitions/798.html"]
  }],
  "totalOccurrences": 1,
  "canonVersion": "v0.1.0",
  "scannedLines": 12,
  "operatingPoint": {"alpha": 0.001, "beta": 0.001},
  "billing": {"cost": 0.15, "tier": "free", "remaining": 999},
  "backedBy": ["T-IB-05", "T-IB-06"]
}
```

## Initial canon coverage (v0.1.0)

- **VC-AI-SSRF-0001** — Server-side request forgery in AI agent fetch tool
- **VC-AI-PROMPT-0001** — Prompt-injection-prone user input concatenation
- **VC-AI-API-0001** — Hardcoded API key or secret
- **VC-AI-TOOL-0001** — Tool with unrestricted shell execution
- **VC-AI-MEM-0001** — Unbounded memory or context accumulation

Canon entries are versioned; full catalog at <https://github.com/viridis-security/vulncanon> as it expands.

## Pricing

Bundled with all paid tiers. Per-scan overage rate: $0.10. See [pricing](https://mcp.viridis-security.com/#pricing).
