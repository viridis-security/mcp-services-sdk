# MCP-10 — Viridis Maxwell (Adversarial Dissipation Defense)

**Tier 2 (target: ship 60 days; promoted from Tier B research direction 2026-05-10)**
**Backed by:** T-IB-09 Adversarial Dissipation Theorem + T-IB-02 Adversarial Landauer Inequality
**Composes with:** MCP-02 (injection detector). MCP-02 *detects*; Maxwell *punishes attacker dissipation*.

## What it does

Standard defenses pay defender's cost (per T-IB-02: `log₂(1/α)` Landauer-quanta per bit protected). Maxwell adds an **asymmetric** layer: the legitimate user's cost stays at the standard floor, but the attacker's cost is multiplied by a configurable `M ≥ 1` (the **Maxwell amplification factor**).

The asymmetry lives in three primitives:

1. **Adaptive proof-of-work challenges** — when MCP-02 flags an input as suspicious, Maxwell returns a PoW puzzle. Legitimate retry → 1 puzzle solved → ~milliseconds. Attacker probing 10K times → 10K puzzles → minutes-to-hours of CPU. PoW difficulty scales with injection probability.
2. **Decoy honeypots** — agents register honeypot actions that look like high-value moves. Attackers triggering them eat poisoned responses that amplify their reconnaissance cost (deliberately wrong information, time-delayed responses, IP-throttle escalation).
3. **Dissipation-receipt binding** — agent actions can be bound to receipts that the legitimate principal already paid for via subscription. Replay attacks without the receipt face the full PoW gauntlet at premium difficulty.

## Why it matters

T-IB-09 (✅ Aristotle-verified 2026-05-10, project `f6dd4bcd-…`) proves the formal claim: an attacker capturing N bits under Maxwell defense dissipates `≥ N · M · kB · T · ln 2` joules vs. the unprotected baseline of `N · kB · T · ln 2`. Concretely:

| M | Per-bit attacker cost relative to baseline | Use case |
|---|---|---|
| 1 (off) | 1× | No Maxwell defense (standard MCP-02 only) |
| 10 | 10× | Default — sufficient against script-kiddie automation |
| 1,000 | 1,000× | High-value agent actions (financial, treasury, multi-sig) |
| 10⁶+ | 10⁶× | Premium tier — attacks become thermodynamically irrational at any scale |

The corollary (T-IB-09d, attack-irrationality threshold) shows: an attack is energetically irrational when `M · kB · T · ln 2 > V` where V is the attacker's per-bit valuation. Maxwell makes M tunable; for a given V, we can configure a defense that makes the attack provably unprofitable.

## API

### Tool: `maxwell.challenge`

Issued by the customer's agent (or the customer's `MCP-02` integration) when an input scores above a configured threshold. Returns a PoW challenge tuned to the threat level.

**Request:**
```json
{
  "agentId": "string (registered envelope ID)",
  "requestId": "string (correlation ID for the original suspicious request)",
  "injectionProbability": 0.0,
  "amplification": "low | medium | high | extreme"
}
```

**Response:**
```json
{
  "challengeId": "ch_abc123...",
  "scheme": "argon2id-pow",
  "params": { "memory": 65536, "iterations": 4, "parallelism": 1, "saltB64": "...", "targetBitsZero": 22 },
  "expiresAt": "2026-05-10T12:34:56Z",
  "estimatedCostMs": { "legitimate": 100, "attacker_per_attempt": 100 }
}
```

The `targetBitsZero` and `iterations` parameters are tuned to the requested amplification:

| Amplification | targetBitsZero | iterations | M (approx) |
|---|---|---|---|
| `low` | 16 | 2 | 10 |
| `medium` | 20 | 4 | 100 |
| `high` | 24 | 6 | 1,000 |
| `extreme` | 28 | 10 | 10⁶ |

### Tool: `maxwell.verify`

**Request:**
```json
{
  "challengeId": "ch_abc123...",
  "solution": "string (PoW solution)",
  "receipt": "string (optional dissipation-receipt token)"
}
```

**Response:**
```json
{
  "verdict": "valid | invalid | expired | replay",
  "remainingChallenges": 4,
  "actionAuthorized": true
}
```

### Tool: `maxwell.decoy`

Registers a honeypot action. When triggered (request matches the decoy spec but lacks a receipt), Maxwell returns deliberately misleading content + escalates IP/account observability.

**Request:**
```json
{
  "agentId": "string",
  "decoyName": "treasury_drain_attempt",
  "triggerSignature": "regex or structured spec",
  "responseTemplate": "string (the misleading response)",
  "escalation": ["log", "throttle", "alert", "blackhole"]
}
```

### Tool: `maxwell.bind`

Issues a dissipation-receipt token for a legitimate principal. Subsequent agent actions presenting the receipt skip PoW (legitimate users); actions without it face full Maxwell.

**Request:**
```json
{
  "agentId": "string",
  "principalId": "string",
  "scope": ["read", "write", "transfer"],
  "ttlSec": 3600
}
```

**Response:** `{ "receipt": "drr_xyz...", "expiresAt": "..." }`

## Pricing

Bundled with MCP-02 in **Growth tier and above**:

| Tier | Maxwell access |
|---|---|
| Free | — (not included) |
| Starter ($49/mo) | — (not included) |
| Growth ($299/mo) | `low` + `medium` amplification, 10K challenges/mo included |
| Scale ($1,499/mo) | All amplification levels, 1M challenges/mo |
| Enterprise | Custom amplification + dissipation receipts + decoy infrastructure |

Standalone enterprise contracts available starting at $25K/yr for high-value agent deployments (treasury management, multi-sig, autonomous trading) where the formal asymmetry guarantee is the differentiator.

## Composability with MCP-02

The intended integration pattern:

```typescript
// Agent's input handler
const detect = await viridis.injection.detect({ input, certainty: "standard", agentId });

if (detect.recommendedAction === "reject") {
  // Hard block: don't even issue a challenge.
  return refuse();
}

if (detect.recommendedAction === "sanitize" || detect.verdict === "suspicious") {
  // Maxwell layer: legitimate retry costs ms; automated probing costs minutes.
  const challenge = await viridis.maxwell.challenge({
    agentId, requestId,
    injectionProbability: detect.probability,
    amplification: detect.bitsAtRisk > 16 ? "high" : "medium",
  });
  // Return challenge to client; client must solve before retrying.
  return { needsChallenge: challenge };
}

// Clean: proceed normally.
return process(input);
```

For `maxwell.bind`-protected actions, the legitimate principal includes a receipt (issued at subscription start or on first use); subsequent calls within the receipt's TTL skip Maxwell entirely. Replay attacks attempting to use a captured receipt face full challenge difficulty + receipt-revocation upon detection.

## Status

- [x] T-IB-09 Lean stub authored
- [x] T-IB-09 submitted to Aristotle (project `f6dd4bcd-b9f2-4818-940f-c6f52fd360c0`)
- [x] **T-IB-09 ✅ PROVED by Aristotle (2026-05-10) — 4/4 theorems verified, standard axioms only**
- [x] Service scaffold (this directory)
- [x] PoW challenge implementation (Argon2id)
- [ ] Decoy infrastructure
- [ ] Receipt-binding service
- [ ] Storage layer (Postgres + Redis)
- [ ] Integration tests with MCP-02
- [ ] DO App Platform deployment
