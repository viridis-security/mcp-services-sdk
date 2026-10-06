<!-- SPDX-License-Identifier: Apache-2.0 -->

# Proposed private WP-6 changes — not implemented

This plan uses observable requirements, not assumed private method names or a fabricated HTTP schema. The blocked adapter tests in `tests/test_hosted_contract_stubs.py` are specifications only.

| Area | Required private change | Acceptance evidence |
| --- | --- | --- |
| Verify path | After authentication, context, expiry and work checks, atomically consume the challenge identity in the authoritative shared store until expiry. Fail closed on store failure; invalid work must not consume state. | Two workers race the same valid solution: exactly one acceptance; replay fails. Expired state is bounded and reclaimed. |
| Receipt lifecycle | Bind principal/action/scope/expiry and any required challenge state according to the confirmed contract. Implement issue, verification and revocation. A detected captured-receipt replay must trigger the documented full-difficulty path and revocation. | Local end-to-end issue/use/revoke and captured-receipt scenarios; no real billing/payment. |
| Argon2id work | Confirm byte encoding, salt handling, memory units, Argon2 version, iteration/parallelism semantics and target comparison. Test independently generated known vectors, not a SHA-256 proxy. | Wrong algorithm/parameters fail; all four documented profiles match exact configured parameters. No inferred joule/M guarantee. |
| Difficulty client | Confirm endpoint/version/auth/request/response contract first. Explicit opt-in transport; bounded timeouts; validate remote difficulty; local fallback on unavailable or invalid response. Never let remote response choose arbitrary URLs. | Mock transport success/error/timeout/malformed response and local fallback; reference default remains offline. |
| Payable alias | Preserve configured, owned payable URL independently of Host/Forwarded headers and user input. | Fixture request-header spoofing cannot change quote binding; fake-payment path only. |
| Existing reference | Preserve the included 17-test contract and wire format. The independently reviewed standalone replay fix may require a separately agreed synchronization scope. | Original 17 tests green; hosted tests must not be substituted with reference results. |
| Public claims | Separate SHA-256 reference from confirmed hosted capabilities. Apply approved WP-2 conditional model wording. | Claim → exact artifact table and actual local hosted acceptance output. |

Unskipping the tests requires a named private source commit, an isolated harness and the exact API contract. Merely supplying fabricated observation dictionaries would not satisfy acceptance. Re-running Aristotle and all production or payment operations remain outside this plan.
