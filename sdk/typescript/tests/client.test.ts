import { afterEach, describe, expect, it, vi } from "vitest";
import { ViridisMCP, ViridisMCPError } from "../src/index";
import type { InjectionDetectResult } from "../src/index";

// Synthetic client-interface fixtures, not captured or accepted hosted responses.
const fixture: InjectionDetectResult = {
  verdict: "suspicious",
  probability: 0.5,
  bitsAtRisk: 8,
  operatingPoint: { alpha: 0.1, beta: 0.2 },
  matchedPatterns: ["local-fixture"],
  recommendedAction: "sanitize",
  explainabilityToken: "local-fixture-token",
  billing: { cost: 0, tier: "local-fixture", remaining: 0 },
};

function mockSuccess() {
  const fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => fixture,
  });
  vi.stubGlobal("fetch", fetch);
  return fetch;
}

afterEach(() => vi.unstubAllGlobals());

describe("local SDK transport contract; no hosted requests", () => {
  it("constructs without making a request", () => {
    const fetch = vi.fn(() => {
      throw new Error("Unexpected request during local initialization");
    });
    vi.stubGlobal("fetch", fetch);
    const client = new ViridisMCP({ apiKey: "local-fixture-key" });
    expect(typeof client.injection.detect).toBe("function");
    expect(fetch).not.toHaveBeenCalled();
  });

  it("serializes the requested POST, headers and optional fields", async () => {
    const fetch = mockSuccess();
    const client = new ViridisMCP({ apiKey: "local-fixture-key" });
    const input = {
      input: "local untrusted text",
      context: "local context",
      certainty: "premium" as const,
      agentId: "local-agent",
    };
    await client.injection.detect(input);
    expect(fetch).toHaveBeenCalledExactlyOnceWith(
      "https://mcp.viridis-security.com/v1/injection/detect",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer local-fixture-key",
          "User-Agent": "viridis-mcp-client/0.1.0",
        },
        body: JSON.stringify(input),
      },
    );
  });

  it("does not invent omitted optional input fields", async () => {
    const fetch = mockSuccess();
    await new ViridisMCP({ apiKey: "local-fixture-key" }).injection.detect({
      input: "local text",
    });
    expect(JSON.parse(fetch.mock.calls[0][1].body)).toEqual({ input: "local text" });
  });

  it("uses a caller-selected endpoint without contacting it", async () => {
    const fetch = mockSuccess();
    await new ViridisMCP({
      apiKey: "local-fixture-key",
      endpoint: "https://example.invalid/local",
    }).injection.detect({ input: "local text" });
    expect(fetch.mock.calls[0][0]).toBe(
      "https://example.invalid/local/v1/injection/detect",
    );
  });

  it("returns the successful JSON fixture without rewriting it", async () => {
    mockSuccess();
    const result = await new ViridisMCP({ apiKey: "local-fixture-key" })
      .injection.detect({ input: "local text" });
    expect(result).toBe(fixture);
  });

  it("retains non-success HTTP status and text in the SDK error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: false,
      status: 429,
      text: async () => "local fixture rejection",
    }));
    const error = await new ViridisMCP({ apiKey: "local-fixture-key" })
      .injection.detect({ input: "local text" })
      .catch((reason: unknown) => reason);
    expect(error).toBeInstanceOf(ViridisMCPError);
    expect(error).toMatchObject({
      name: "ViridisMCPError",
      status: 429,
      message: "local fixture rejection",
    });
  });

  it("propagates transport failure without inventing a successful result", async () => {
    const failure = new TypeError("local fixture transport failure");
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(failure));
    await expect(new ViridisMCP({ apiKey: "local-fixture-key" })
      .injection.detect({ input: "local text" })).rejects.toBe(failure);
  });
});
