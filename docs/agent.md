# The Agent Class
`multimodal_agent.agent_core.MultiModalAgent`  

The main class powering multimodal communication with Gemini.

## Initialization

```python
from multimodal_agent.agent_core import MultiModalAgent

agent = MultiModalAgent(model="gemini-2.5-flash")
```
Arguments:
| Arg  | Type | Default | Description |
| ---- | ---- | ------- | ----------------- |
| model | str |   "gemini-2.5-flash"  | Gemini model name | 
| api_version | str | "v1"  | Gemini API version |
| client | genai.Client | None | Inject custom client (used for testing)|
---



## Methods
### `ask(prompt: str) -> str`
Sends a text-only request.

```python
agent.ask("What is recursion?")
```
### `ask_with_image(prompt: str, image: Part) -> str`
Sends an image + text multimodal prompt.

```python
image = load_image_as_part("photo.jpg")
agent.ask_with_image("Describe this image.", image)
```
### `chat()`
Starts a REPL (interactive loop).

```bash
agent chat
```
## Retry Logic
All request methods use:

``` python
safe_generate_content()
``` 

Which includes:

* Exponential backoff

* Retryable errors (503 overload)

* `RetryableError` and `NonRetryableError` exceptions

## Exceptions Raised
* `RetryableError`

* `NonRetryableError`
* `AgentError (base class)`
