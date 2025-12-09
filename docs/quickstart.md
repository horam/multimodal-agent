# Quickstart

Below are the minimum examples needed to use the agent.



```python
from multimodal_agent import MultiModalAgent

agent = MultiModalAgent()
resp = agent.ask("Tell me something interesting about the universe.")
print(resp.text)
```

## Image + Text Generation

```python
from multimodal_agent import MultiModalAgent
from multimodal_agent.utils import load_image_as_part

agent = MultiModalAgent()

image = load_image_as_part("cat.jpg")
resp = agent.ask_with_image("Describe this cat.", image)

print(resp.text)
```

## CLI Quickstart

```bash
agent ask "hello world"
agent image photo.jpg "what do you see?"
agent chat
agent --version
agent --debug ask "hello"
```

### **Choosing Models**

You can override the default model from CLI or config:
```bash
agent config set-chat-model gemini-2.5-flash
```

## Error Handling Example

```python
from multimodal_agent import MultiModalAgent
from multimodal_agent.errors import AgentError

agent = MultiModalAgent()

try:
    print(agent.ask("hello").text)
except AgentError as e:
    print("The request failed:", e)
```

## JSON Response Mode (v0.3.0)

The agent can return structured JSON:

```python
from multimodal_agent import MultiModalAgent

agent = MultiModalAgent(enable_rag=False)

resp = agent.ask(
    "Return a JSON person object.",
    response_format="json"
)

print(resp.data)  # → Python dict
```

`<strong>`Supported behavior`</strong>`

- Accepts raw JSON responses
- Removes ```json fenced blocks
- Fallback to {"raw": "..."}
- Works identically in offline FakeResponse mode
- Returns an AgentResponse with:

```python
resp.text  # original text
resp.data  # parsed JSON dict
resp.usage # token usage (dict or None)
```
