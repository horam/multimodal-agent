# Quickstart

Below are the minimum examples needed to use the agent.


## Text Generation

```python
from multimodal_agent import MultiModalAgent

agent = MultiModalAgent()
response = agent.ask("Tell me something interesting about the universe.")
print(response)
```
## Image + Text Generation
```python
from multimodal_agent import MultiModalAgent
from multimodal_agent.utils import load_image_as_part

agent = MultiModalAgent()

image = load_image_as_part("cat.jpg")
response = agent.ask_with_image("Describe this cat.", image)

print(response)
```
## CLI Quickstart
``` bash
agent ask "hello world"
agent image photo.jpg "what do you see?"
agent chat
agent --version
agent --debug ask "hello"
```
## Error Handling Example
``` python
from multimodal_agent import MultiModalAgent
from multimodal_agent.errors import AgentError

agent = MultiModalAgent()

try:
    print(agent.ask("hello"))
except AgentError as e:
    print("The request failed:", e)
```
## JSON Response Mode (v0.3.0)
The agent can return structured JSON instead of plain text:

```python
from multimodal_agent import MultiModalAgent

agent = MultiModalAgent(enable_rag=False)

data = agent.ask(
    "Return a JSON person object.",
    response_format="json"
)
print(data)  # → Python dict
```
Supported behaviors:

- Accepts raw JSON

- Removes ```json fenced blocks

- Falls back to {"raw": "..."}

- Works in offline FakeResponse mode
