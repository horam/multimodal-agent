# JSON Response Mode

Since **v0.3.0**, Multimodal-Agent supports structured JSON output via:

```python
agent.ask(question, response_format="json")
```
## How it works
- The Gemini client is instructed to return JSON-compatible output.

- The agent parses the response into a Python `dict`.

- Markdown fences (`json ... `) are automatically stripped.

- Invalid JSON falls back to:

```python
{"raw": "<original text>"}
```
This ensures the agent never crashes on malformed JSON.

---
### Example
```python
agent = MultiModalAgent(enable_rag=False)

result = agent.ask(
    "Return a movie object with title and year.",
    response_format="json",
)

print(result)
```
Output:

```python
{"title": "The Matrix", "year": 1999}
```
---

### JSON from Images
```python
from multimodal_agent.utils import load_image_as_part

img = load_image_as_part("cat.jpg")

result = agent.ask_with_image(
    "Describe this image as JSON.",
    img,
    response_format="json",
)

print(result)
```
---
### Offline Mode
If no 'GOOGLE_API_KEY' is set:

```bash
export GOOGLE_API_KEY=""
```
The agent uses FakeResponse but still returns JSON:

```python
{"raw": "FAKE_RESPONSE: ..."}
```
