# Viridis MCP + AutoGen / Microsoft AutoGen

AutoGen agents pass messages between each other; injection attempts can travel through that messaging layer. Drop a Viridis pre-check on every incoming message.

## Python — Microsoft AutoGen v0.4+ (autogen-core)

```python
from autogen_core.components import RoutedAgent, message_handler
from viridis_mcp_client import ViridisMCP

viridis = ViridisMCP(api_key=os.environ["VIRIDIS_API_KEY"])

class GuardedAgent(RoutedAgent):
    def __init__(self, description: str):
        super().__init__(description)

    @message_handler
    async def handle_message(self, message: str, ctx) -> str:
        # Inbound message guard
        r = viridis.injection.detect(input=message, certainty="standard")
        if r.recommended_action == "reject":
            return f"[Viridis] Refused: injection detected (p={r.probability})"
        # ... your agent logic here
        return await self.process(message)
```

## Python — older AutoGen (ConversableAgent)

```python
from autogen import ConversableAgent
from viridis_mcp_client import ViridisMCP

viridis = ViridisMCP(api_key=os.environ["VIRIDIS_API_KEY"])

def message_filter(message: str) -> str | None:
    r = viridis.injection.detect(input=message, certainty="standard")
    if r.recommended_action == "reject":
        return None  # AutoGen will skip; or raise for hard failure
    return message

agent = ConversableAgent(
    name="my_agent",
    system_message="...",
    # Use a custom reply function that filters first
)
agent.register_reply(
    trigger=lambda x: True,
    reply_func=lambda recipient, messages, sender, config: (
        True,
        viridis_check_or_pass(messages[-1]["content"])
    ),
)
```

## Multi-agent compositional auditing (T-IB-04 verified)

When you have an agent chain like `UserAgent → CoordinatorAgent → ToolAgent`, register each agent's authorized output envelope via MCP-01 envelope registry (shipping shortly), and use MCP-04 composability auditor (Tier 2) to verify the chain is attribution-safe.

For now: gate each inter-agent message with `viridis.injection.detect`. Per **T-IB-04 Composability Attribution Theorem** (formally verified in Lean 4 by Aristotle), this gives you a linear-in-chain-length audit cost.

## Pricing

| AutoGen scale | Tier |
|---|---|
| Single-agent prototype | Free |
| 2-3 agents, dev use | Starter |
| 5-10 agents, production | Growth |
| Multi-tenant AutoGen-based product | Scale + Maxwell defense |
