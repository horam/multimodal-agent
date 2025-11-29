# JSON Response Mode

Since **v0.3.0**, Multimodal-Agent supports structured JSON output via:

```python
agent.ask(question, response_format="json")
```
## How it works
The agent instructs the model to return raw JSON without backticks.

- The final result is always an AgentResponse object.

- Parsed JSON is stored in response.data (a Python dict or None).

- The raw text returned by the model is always accessible via response.text.

- Markdown fences such as:

```json
{ ... }
```
are automatically stripped during parsing.

- Invalid or malformed JSON cleanly falls back to:

```python
{"raw": "<original text>"}
```
This ensures JSON mode never crashes.

## Example
```python
from multimodal_agent import MultiModalAgent

agent = MultiModalAgent(enable_rag=False)

result = agent.ask(
    "Return a movie object with title and year.",
    response_format="json",
)

print(result.data)   # parsed dict
print(result.text)   # raw text from the model
```
Output:

```python
{"title": "The Matrix", "year": 1999}
```
## JSON from Images
```python
from multimodal_agent import MultiModalAgent
from multimodal_agent.utils import load_image_as_part

agent = MultiModalAgent(enable_rag=False)
img = load_image_as_part("cat.jpg")

result = agent.ask_with_image(
    "Describe this image as JSON.",
    img,
    response_format="json",
)

print(result.data)
```
## Offline Mode
If no GOOGLE_API_KEY is set:

```bash
export GOOGLE_API_KEY=""
```
The agent switches to FakeResponse simulation mode.

JSON mode still returns an AgentResponse, and .data becomes:

```python

result = agent.ask("hello", response_format="json")
print(result.data)
```
Output:

```python
{"raw": "FAKE_RESPONSE: hello"}
```
JSON mode behaves consistently across online and offline scenarios.