# RAG System (Retrieval-Augmented Generation)

The RAG system provides persistent memory storage using SQLite.

Features:

- Message chunk storage
- Embedding storage
- Cosine similarity retrieval
- Integration with `ask()` and `chat()`
- Project profile storage (v0.6.0)

Memory DB location:
```bash
~/.multimodal_agent/memory.db
```


## How RAG Works

1. Text is split into normalized chunks.
2. Each chunk is embedded using Gemini embeddings.
3. Embeddings stored in `embeddings` table.
4. Queries embed the input text.
5. Cosine similarity finds most relevant chunks.
6. Agent uses them to augment responses.


## Project Learning Integration (v0.6.0)

`ingest_style_into_rag()` stores:

- package metadata
- architecture style
- lint profile
- Dart structure summary

This allows queries like:

```bash
POST /memory/search {"query": "bloc architecture"}
```

to retrieve project structure insights.


## Storage Layout

- chunks
- embeddings
- sessions
- project_profiles (v0.6.0)



## Fake Embedding Mode for Tests

Real embeddings are disabled during tests.

You can monkeypatch:

```python
monkeypatch.setattr(
    "multimodal_agent.core.embedding.embed_text",
    lambda text, model: [0.1, 0.2, 0.3],
)
```
This ensures:

- no API calls
- consistent deterministic vectors

## **Clearing Memory**

```bash
agent clear
```
Resets all tables.

### **Example Query:**
```python
results = rag.search_similar("json formatting", model="default", top_k=5)
```
Returns list of tuples:

```python
[(0.92, Chunk(...)), ...]
```
