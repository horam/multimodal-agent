# Code Examples

## Simple Text Request

```python
from multimodal_agent.agent_core import MultiModalAgent

agent = MultiModalAgent()
print(agent.ask("hello"))
```
## Custom Model
```bash
agent --model gemini-pro ask "summarize transformers"
```
## Multimodal Request
```python
from multimodal_agent.utils import load_image_as_part
from multimodal_agent.agent_core import MultiModalAgent

agent = MultiModalAgent()
img = load_image_as_part("cat.jpg")

print(agent.ask_with_image("describe this", img))
```
## Error Handling Example
```python
from multimodal_agent.agent_core import MultiModalAgent
from multimodal_agent.errors import AgentError

agent = MultiModalAgent()

try:
    print(agent.ask("hello"))
except AgentError as e:
    print("The request failed:", e)
```