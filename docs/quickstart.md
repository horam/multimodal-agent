# Quickstart

## Text Generation

```python
from multimodal_agent.agent_core import MultiModalAgent

agent = MultiModalAgent()
print(agent.ask("Tell me a fun fact about space."))
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

agent ask "What is recursion?"
agent image photo.jpg "describe this"
agent chat
agent --version
```