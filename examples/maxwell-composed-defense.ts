/**
 * Composed defense pattern: MCP-02 detect + MCP-10 Maxwell challenge.
 *
 * OPEN-SOURCE (Apache 2.0). Customers can read, copy, modify, redistribute.
 */
import { ViridisMCP } from "@viridis/mcp-client";

const viridis = new ViridisMCP({ apiKey: process.env.VIRIDIS_API_KEY! });

async function handleAgentInput(input: string, agentId: string, requestId: string) {
  // Step 1: detect injection (MCP-02)
  const detect = await viridis.injection.detect({ input, agentId, certainty: "standard" });

  if (detect.recommendedAction === "reject") {
    // Hard block — high confidence attack
    return { ok: false, reason: "rejected", probability: detect.probability };
  }

  if (detect.verdict === "suspicious") {
    // Maxwell: cheap for legitimate retry, expensive for automated probing
    const ch = await viridis.maxwell.challenge({
      agentId,
      requestId,
      injectionProbability: detect.probability,
      amplification: detect.bitsAtRisk > 16 ? "high" : "medium",
    });
    return { ok: false, needsChallenge: ch };
  }

  // Clean: proceed
  return { ok: true, processInput: input };
}

// Server side — verify challenge solution before re-running detection
async function handleChallengeSolution(challengeId: string, solution: string) {
  const v = await viridis.maxwell.verify({ challengeId, solution });
  return v.actionAuthorized;
}
