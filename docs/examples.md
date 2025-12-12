# Code Examples

This page provides small, practical examples showing how to use the Multimodal-Agent
via **Python API**, **CLI**, **image queries**, **RAG**, and **Flutter code generation** (v0.8.0+).


## Simple Text Request

```python
from multimodal_agent import MultiModalAgent

agent = MultiModalAgent()

resp = agent.ask("Explain state management in Flutter.")
print(resp.text)
```


## JSON Mode
```python
resp = agent.ask("return a small object", response_format="json")
print(resp.data)
```

Output:
```json
{
  "title": "Example",
  "value": 42
}
```


## Image + Text Queries

```python
from multimodal_agent.utils import load_image_as_part

agent = MultiModalAgent()

image = load_image_as_part("cat.jpg")
resp = agent.ask_with_image("What do you see?", image)

print(resp.text)
```

## RAG: Adding Messages Manually
```python
agent.rag_store.add_logical_message(
    content="This project uses Riverpod for state management",
    role="note",
    session_id="flutter-app",
    source="manual"
)
```
Query using memory:
```python
resp = agent.ask("What state management do we use?")
print(resp.text)
```

## CLI Examples

**Ask a question**
```bash
agent ask "What is dependency injection?"
```

**Ask with JSON mode**
```bash
agent ask "give sample json" --json
```

**Ask with an image**
```bash
agent image photo.png "describe this"
```

**Interactive chat**
```bash
agent chat
```

## Flutter Code Generation (v0.8.0)

**Generate a stateless widget**
```bash
agent gen widget UserCard
```

Produces:
```bash
lib/widgets/user_card.dart
```

**Generate a stateful widget**
```bash
agent gen widget Counter --stateful
```

**Generate a screen**
```bash
agent gen screen HomeScreen
```

**Generate a Dart model**
```bash
agent gen model UserProfile
```

Use --override to overwrite:
```bash
agent gen widget UserCard --override
```


## Project Learning Example
```bash
agent learn-project my_flutter_app/
```

Load profile again:
```bash
agent show-project project:my_flutter_app
```

## Offline Mode Example

If your environment has no API key, the agent returns deterministic fake responses:
```bash
unset GOOGLE_API_KEY
agent ask "hello"
```

Output:
```bash
FAKE_RESPONSE: hello
```

Useful for:
-	CI pipelines
-	Local tests
-	Environments without network


## FastAPI Server Example

Run server:
```bash
agent server --port 9000
```

Query:
```bash
curl -X POST http://localhost:9000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello"}'
```

## Full Minimal Python Script
```python
from multimodal_agent import MultiModalAgent

agent = MultiModalAgent(model="gemini-2.5-flash")

resp = agent.ask("Summarize Flutter architecture.")
print(resp.text)

resp = agent.ask("give json", response_format="json")
print(resp.data)

img = load_image_as_part("ui.png")
resp = agent.ask_with_image("Describe this UI", img)
print(resp.text)
```