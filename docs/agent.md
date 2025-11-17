# The Agent Class

The main class powering multimodal communication with Gemini.

## Initialization

```python
from multimodal_agent.agent_core import MultiModalAgent

agent = MultiModalAgent(model="gemini-2.5-flash")
```
---
## Methods

### ask(prompt: str) -> str
Send a text-only request.


### ask_with_image(prompt: str, image: Part) -> str
Send an image + prompt.

### chat()
Interactive REPL loop.


## Retry Logic
All requests go through:

    safe_generate_content()

* exponential backoff

* retryable vs non-retryable errors

* structured custom exceptions