
# Code Examples

### Simple example

```python
agent = MultiModalAgent()
print(agent.ask("hello"))
```
### Using custom model
```python
agent --model gemini-pro ask "explain transformers"
```
### Error handling example
```python
from multimodal_agent.errors import AgentError

try:
    agent.ask("hello")
except AgentError as e:
    print("Request failed:", e)
```

