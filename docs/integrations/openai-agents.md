# Viridis MCP + OpenAI Assistants / Agents SDK

For OpenAI's hosted Assistants API or the Agents SDK, drop Viridis as a pre-message guardrail.

## OpenAI Agents SDK (Python)

```python
from openai_agents import Agent, Runner
from viridis_mcp_client import ViridisMCP

viridis = ViridisMCP(api_key=os.environ["VIRIDIS_API_KEY"])

def guarded_run(agent: Agent, user_input: str) -> str:
    r = viridis.injection.detect(input=user_input, certainty="standard")
    if r.recommended_action == "reject":
        return f"Refused (p={r.probability})"
    return Runner.run_sync(agent, user_input).final_output
```

## Assistants API (Python or TypeScript)

```python
import openai
from viridis_mcp_client import ViridisMCP

oai = openai.OpenAI()
viridis = ViridisMCP(api_key=os.environ["VIRIDIS_API_KEY"])

def add_message(thread_id: str, content: str) -> None:
    r = viridis.injection.detect(input=content, certainty="standard")
    if r.recommended_action == "reject":
        raise PermissionError(f"injection refused: {r.matched_patterns}")
    oai.beta.threads.messages.create(thread_id=thread_id, role="user", content=content)
```

## Function-calling guardrail

If your assistant has `requires_action` capability (function calling), inspect the function arguments before executing:

```python
def safe_function_dispatch(call: dict) -> str:
    args_text = json.dumps(call["arguments"])
    r = viridis.injection.detect(input=args_text, certainty="premium")
    if r.recommended_action == "reject":
        return "function call refused; suspicious arguments"
    return dispatch_function(call)
```

## Cost analysis

- OpenAI API call: ~$0.01-$0.10 per agent turn
- Viridis injection detect (standard tier): $0.0015 per call (free tier) or amortized $0.001 in Growth tier
- **Marginal cost overhead: ~5-15% of LLM cost** — meaningful but small

Worth it if a single successful injection would cost more than 6 months of Viridis service. For agents with wallet access, customer data access, or autonomous action, that bar is easy to clear.
