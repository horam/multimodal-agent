# Quickstart

### Text generation


```python
from multimodal_agent.agent_core import MultiModalAgent

agent = MultiModalAgent()
print(agent.ask("Tell me something interesting."))
Image + text
python
Copy code
from multimodal_agent.agent_core import MultiModalAgent
from multimodal_agent.utils import load_image_as_part

agent = MultiModalAgent()

image = load_image_as_part("cat.jpg")
print(agent.ask_with_image("Describe this cat.", image))
```