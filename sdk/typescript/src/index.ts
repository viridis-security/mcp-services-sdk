/**
 * Viridis MCP Client SDK
 *
 * Open-source (Apache 2.0). Hosted endpoint at https://mcp.viridis-security.com.
 * Source: https://github.com/viridis-security/mcp-services
 *
 * Backing theorems (Aristotle-verified):
 *   T-IB-01..07, see https://github.com/viridis-security/corpus
 */

export interface ViridisMCPConfig {
  apiKey: string;
  endpoint?: string;
}

export interface InjectionDetectInput {
  input: string;
  context?: string;
  certainty?: "quick" | "standard" | "premium";
  agentId?: string;
}

export interface InjectionDetectResult {
  verdict: "clean" | "suspicious" | "attack";
  probability: number;
  bitsAtRisk: number;
  operatingPoint: { alpha: number; beta: number };
  matchedPatterns: string[];
  recommendedAction: "allow" | "sanitize" | "reject" | "escalate";
  explainabilityToken: string;
  billing: { cost: number; tier: string; remaining: number };
}

export class ViridisMCP {
  private apiKey: string;
  private endpoint: string;

  constructor(config: ViridisMCPConfig) {
    this.apiKey = config.apiKey;
    this.endpoint = config.endpoint ?? "https://mcp.viridis-security.com";
  }

  injection = {
    detect: async (input: InjectionDetectInput): Promise<InjectionDetectResult> => {
      const res = await fetch(`${this.endpoint}/v1/injection/detect`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${this.apiKey}`,
          "User-Agent": "viridis-mcp-client/0.1.0",
        },
        body: JSON.stringify(input),
      });
      if (!res.ok) {
        throw new ViridisMCPError(await res.text(), res.status);
      }
      return res.json();
    },
  };

  // canon, envelope, composability, etc. SDKs added as their MCPs ship
}

export class ViridisMCPError extends Error {
  constructor(message: string, public status: number) {
    super(message);
    this.name = "ViridisMCPError";
  }
}
