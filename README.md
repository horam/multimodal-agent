# **Multimodal-Agent**

*A lightweight, production-ready multimodal wrapper for Google Gemini with optional RAG, image input, JSON mode, and a clean CLI.*

---

## Features

- 🔹 **Text generation (Gemini)**
- 🔹 **Image + text multimodal input**
- 🔹 **Retry logic with exponential backoff**
- 🔹 **JSON response mode** (`response_format="json"`)
- 🔹 **Dummy offline mode (no API key required)**
- 🔹 **Clean CLI (`agent`)**
- 🔹 **90%+ test coverage**
- 🔹 **Chunking + RAG store (simple & embeddable)**
- 🔹 **Session history + memory**
- 🔹 **Extensible architecture for VS Code / Flutter integration**

---

## Installation

```bash
pip install multimodal-agent
```

Or install a specific version:

```bash
pip install multimodal-agent==0.3.0
```

### Setup API Key (Optional)

If you want real Gemini output:

```bash
export GOOGLE_API_KEY="your-key-here"
```

Without a key, the package still works using offline FakeResponse for testing & debugging.

## Basic Usage

```python
from multimodal_agent import MultiModalAgent

agent = MultiModalAgent(enable_rag=False)

print(agent.ask("Explain quantum physics to me."))
```

## Ask With Image

```python
from multimodal_agent import MultiModalAgent
from multimodal_agent.utils import load_image_as_part

agent = MultiModalAgent(enable_rag=False)

image = load_image_as_part("cat.jpg")
print(agent.ask_with_image("Describe this image.", image))
```

## JSON Response Mode

Ask for strict JSON:

```python
response = agent.ask(
    "Give me a JSON summary of The Matrix.",
    response_format="json",
)

print(response)
```

Output example:

```python
{"title": "The Matrix", "year": 1999}
```

Supports:
✔ Raw dict return
✔ JSON inside markdown fences
✔ Invalid JSON fallback → {"raw": "..."}'
✔ Works in offline mode (FakeResponse)

## RAG Mode (Optional)

Enable RAG:

```python
agent = MultiModalAgent(enable_rag=True)
agent.ask("First message")
agent.ask("Second message referencing the first")
```

RAG stores:

- chunked logs
- embeddings
- search similarity

This makes your CLI "memory aware".

## CLI Usage

```bash
agent
```

Then interactive chat:

```bash
You: hello
Agent: ...
```

Quit:

```bash
You: exit
```

## Running Tests

```bash
make test
make coverage
```

Test coverage: ~91%

## Architecture Overview

agent_core.py — main agent logic

chunking.py — text chunking & normalization

embedding.py — embedding wrappers

rag_store.py — vector search store

cli.py — command line interface

utils.py — image loading, memory, history helpers

## Roadmap

v0.3.1 — Token usage logging

v0.4.0 — Flutter-friendly structured outputs

v0.5.0 — VS Code extension alpha

v0.6.0 — Android Studio plugin

v1.0.0 — Public launch (website + demos + docs)

# License

MIT License.
