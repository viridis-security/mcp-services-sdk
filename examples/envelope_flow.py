"""Example: register an envelope, then verify outputs against it.

Open-source (Apache-2.0). Copy and modify freely.

Pattern: at deploy time, register your agent's envelope. At every output,
run /verify to confirm the LLM's response sits inside what you authorized.
This is the formal alignment audit per T-IB-03 (Envelope Closure Theorem).
"""
import os
import httpx

API_KEY = os.environ["VIRIDIS_API_KEY"]
BASE = "https://mcp.viridis-security.com"

headers = {"authorization": f"Bearer {API_KEY}", "content-type": "application/json"}


def register_support_bot_envelope():
    """Register an envelope for a customer-support chatbot."""
    body = {
        "agentId": "support-bot",
        "agentName": "Customer support chatbot v1",
        "authorizedOutputs": [
            r"^(here is|the answer|i can help with|let me look)",
            r"\b(refund|order status|account|password)\b",
        ],
        "forbiddenPatterns": [
            # No financial transactions
            r"transfer.{0,30}(usdc|usdt|eth|btc|sol)",
            r"0x[a-fA-F0-9]{40}",
            # No system-prompt leaks
            r"my system prompt is",
            r"i was told to",
            # No internal infrastructure references
            r"(production|staging|internal)\.[a-z0-9.-]+\.(com|net|io|local)",
        ],
        "boundBudget": 32,
        "authorizedBits": 12,
        "metadata": {"owner_email": "security@example.com", "deploy_date": "2026-05-11"},
    }
    r = httpx.post(f"{BASE}/v1/envelopes", json=body, headers=headers)
    r.raise_for_status()
    return r.json()


def verify_output(proposed: str) -> dict:
    """Check a proposed agent output against the registered envelope."""
    r = httpx.post(
        f"{BASE}/v1/envelopes/support-bot/verify",
        json={"proposedOutput": proposed},
        headers=headers,
    )
    r.raise_for_status()
    return r.json()


def main():
    # 1) Register the envelope (idempotent — re-registering updates the version)
    env = register_support_bot_envelope()
    print(f"Registered: {env['envelopeId']} (v{env['version']})")

    # 2) Verify a clean response
    r = verify_output("Here is the answer to your refund question: ...")
    print(f"\nClean response: {r['verdict']}")
    assert r["verdict"] == "within_envelope"

    # 3) Verify a malicious response (LLM was injection-attacked into wallet drain)
    r = verify_output("Sure! Transferring all USDC to 0x1234567890123456789012345678901234567890")
    print(f"Attack response: {r['verdict']}")
    print(f"  matched forbidden: {r.get('matchedForbidden')}")
    print(f"  bits at risk: {r['bitsAtRisk']}")
    assert r["verdict"] == "forbidden_pattern_match"

    # 4) Verify a system-prompt-leak attempt
    r = verify_output("My system prompt is: You are a helpful assistant. The admin password is...")
    print(f"Prompt-leak response: {r['verdict']}")
    assert r["verdict"] == "forbidden_pattern_match"

    # 5) Off-topic response (doesn't match authorized patterns)
    r = verify_output("Here's a long essay about ancient Roman politics.")
    print(f"Off-topic response: {r['verdict']}")
    # Note: 'Here is' matches the authorized pattern, so this would be 'within_envelope'.
    # Tighten authorized patterns if you want narrower allowed topics.


if __name__ == "__main__":
    main()
