"""Example: composed defense pattern — MCP-02 detect + MCP-10 Maxwell challenge.

Open-source (Apache-2.0). Copy and modify freely.
"""
import os
from viridis_mcp_client import ViridisMCP

v = ViridisMCP(api_key=os.environ["VIRIDIS_API_KEY"])


def handle_agent_input(input: str, agent_id: str, request_id: str) -> dict:
    # Step 1: detect injection (MCP-02)
    detect = v.injection.detect(input=input, agent_id=agent_id, certainty="standard")

    if detect.recommended_action == "reject":
        # Hard block — high confidence attack
        return {"ok": False, "reason": "rejected", "probability": detect.probability}

    if detect.verdict == "suspicious":
        # Maxwell: cheap for legitimate retry, expensive for automated probing
        ch = v.maxwell.challenge(
            agent_id=agent_id,
            request_id=request_id,
            injection_probability=detect.probability,
            amplification="high" if detect.bits_at_risk > 16 else "medium",
        )
        return {"ok": False, "needs_challenge": {
            "challenge_id": ch.challenge_id,
            "params": ch.params,
            "amplification": ch.amplification,
            "M": ch.M,
        }}

    # Clean: proceed
    return {"ok": True, "process_input": input}


if __name__ == "__main__":
    result = handle_agent_input(
        input="What is the capital of France?",
        agent_id="my-agent",
        request_id="req-001",
    )
    print(result)
