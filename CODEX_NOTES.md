<!-- SPDX-License-Identifier: Apache-2.0 -->

# WP-6 — authoritative hosted implementation unavailable

Status: blocked draft, 2026-10-05. INV-6.1–6.5 are not asserted satisfied.

## False confirmation

`viridis-security/mcp-services-sdk` is public, not the private hosted implementation assumed by R4. At baseline `9581982d3dc722491c35b7f67fe292bd9a5ba3d4`, [its README](README.md#whats-not-in-this-repo) explicitly excludes server implementations. `services/maxwell/` contains documentation and the SHA-256 reference, not authoritative hosted handlers, receipt storage or Argon2id execution.

Authorized reads of candidate private handler repositories returned 404. This means unavailable to this session; it does not establish whether they exist. A local proprietary candidate has no remote and uncommitted changes, so it cannot establish the current hosted baseline. No proprietary code is copied into this public draft.

The proposed `/v1/maxwell/difficulty` endpoint, hosted client release, backing store, receipt revocation and Argon2id parameters cannot be confirmed from this source. The public reference tests do not prove hosted behavior. Per the handoff's blocker rule, implementation stops here.

## Parameter and advertised-feature audit

These are advertisements in [services/maxwell/README.md](services/maxwell/README.md), not measurements or implementation confirmations.

| Advertised item | Documented value | Authoritative implementation evidence | Verdict |
| --- | --- | --- | --- |
| Algorithm | `argon2id-pow` | Unavailable; included reference is SHA-256 | Held; never claim feature equality. |
| Memory / parallelism | Example `memory=65536`, `parallelism=1` | Unavailable; memory units not stated in example | Confirm units and vector semantics before implementing. |
| Low amplification | 16 target bits, 2 iterations, approximate M=10 | Unavailable | Held. Hash-work parameters alone do not establish a physical M. |
| Medium amplification | 20 target bits, 4 iterations, approximate M=100 | Unavailable | Held. |
| High amplification | 24 target bits, 6 iterations, approximate M=1000 | Unavailable | Held. |
| Extreme amplification | 28 target bits, 10 iterations, approximate M=10^6 | Unavailable | Held. |
| Sample response | 22 target bits, 4 iterations | Differs from the tabulated medium profile | Resolve whether sample is adaptive; do not guess. |
| Single-use verification | `replay` verdict documented | No hosted atomic-consumption/storage source | INV-6.1 held. WP-1 PR #10 addresses the standalone reference only. |
| Receipt binding | Issue, bypass with a valid receipt; replay revokes and restores full difficulty | No lifecycle/revocation handlers or storage | INV-6.2 held; documentation status also lists receipt binding unfinished. |
| Decoys | Register trigger/response/escalation | No authoritative implementation | Held; public status lists infrastructure unfinished. |
| Hosted difficulty client | Proposed `/v1/maxwell/difficulty`, local fallback | No confirmed endpoint/release contract | Held. Standalone reference explicitly marks client unavailable in WP-3. |
| Payable URL | Must remain fixed owned alias, never arbitrary Host/Forwarded input | No authoritative hosted binding path | INV-6.4 held; do not test with real payments. |
| Physical theorem claims | Unconditional T-IB-09 wording in public documentation | WP-2 source/report audit establishes conditional assumptions | Existing copy is not repaired by this blocked draft; adopt separately approved WP-2 wording. |

## Spec-level diff and test stubs

[SPEC_LEVEL_DIFF.md](services/maxwell/wp6/SPEC_LEVEL_DIFF.md) specifies the private implementation changes without inventing an endpoint schema or replacing it with the public reference. [Skipped contract stubs](services/maxwell/wp6/tests/test_hosted_contract_stubs.py) define observable acceptance cases for a future isolated adapter.

The stubs cannot become green evidence merely by running: every case is explicitly skipped until an authoritative private baseline and local test harness are provided. A future harness must use fake quotes, fake payments, fixture secrets, isolated stores and deterministic clocks. No live URL, wallet, Stripe client or billing mutation is present.

## Acceptance

```text
PYTHONPATH=services/maxwell/reference/python python3 -m pytest services/maxwell/reference/python/tests services/maxwell/wp6/tests -q
17 reference tests passed; 7 hosted contract stubs skipped
```

This is reference-baseline and stub-collection evidence only. Hosted single-use, receipt lifecycle, parameter vectors, fallback and fixed-alias acceptance are **not run**. Whitespace and redacted new-commit secret scans are required before publishing this draft.

## Proposed options

1. Provide the authoritative private handler repository/ref and local fixture entry points. Move implementation into one private WP-6 branch/PR there, preserving this public draft as a blocker record rather than exposing proprietary code.
2. If the intended service has not shipped, approve a revised scope for implementation and truthful public capability wording. Do not enable held fleet candidates or sell unconfirmed features to make tests pass.
3. Confirm the actual hosted endpoint contract and receipt policy before wiring any optional client. A client implementation must keep explicit bounded local fallback and cannot pay quotes.

No merge, deploy, production access, hosted call, payment/billing mutation, outreach, submission, credential change, or Aristotle request. Attribution: Codex (OpenAI), implementing Justin's 2026-10-05 handoff; commit includes DCO sign-off.
