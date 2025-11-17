# Quickstart

Below are the minimum examples needed to use the agent.


## Text Generation

```python
from multimodal_agent.agent_core import MultiModalAgent

agent = MultiModalAgent()
response = agent.ask("Tell me something interesting about the universe.")
print(response)
```
## Image + Text Generation
```python
from multimodal_agent.agent_core import MultiModalAgent
from multimodal_agent.utils import load_image_as_part

agent = MultiModalAgent()

image = load_image_as_part("cat.jpg")
response = agent.ask_with_image("Describe this cat.", image)

print(response)
```
## CLI Quickstart
```bash
agent ask "hello world"
agent image photo.jpg "what do you see?"
agent chat
agent --version
agent --debug ask "hello"
```
## Error Handling Example
```python
Copy code
from multimodal_agent.agent_core import MultiModalAgent
from multimodal_agent.errors import AgentError

agent = MultiModalAgent()

try:
    print(agent.ask("hello"))
except AgentError as e:
    print("The request failed:", e)
```