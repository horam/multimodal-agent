# multimodal_agent

This module provides the main high-level interface for interacting with Gemini models using text, images, and optional RAG storage.


## Constructor

```python
MultiModalAgent(
    model="gemini-2.0-flash-lite",
    enable_rag=False,
    rag_store=None,
    embedding_model="embedding-001",
)
```
### Methods

`ask(question: str, response_format="text") -> AgentResponse`

Send a text prompt.

```python
resp = agent.ask("hello")
resp.text   # string
resp.usage  # token usage dict
```

JSON example:

```python
resp = agent.ask("give json", response_format="json")
resp.data   # parsed dict
```
``ask_with_image(question: str, image: Part, response_format="text") -> AgentResponse``

Send a question with an image part.

---

``chat(...)``

Multi-turn conversation interface.

---
``AgentResponse``

Returned by all calls:

```python
resp.text   # raw response text
resp.data   # dict for JSON mode, else None
resp.usage  # token metadata
```
---
### Utilities
`load_image_as_part(path)`

Loads an image from disk and converts it into a Gemini-compatible Part.

----

### RAG Components
The agent supports plug-and-play RAG via:

- `rag_store.add_logical_message`

- `rag_store.add_embedding`

- `rag_store.search_similar`

See `docs/rag_store.md` for details.