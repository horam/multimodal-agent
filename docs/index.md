# Multimodal-Agent

A lightweight, production-ready wrapper around **Google Gemini** with:
- Robust CLI(`agent`)
- RAG memory
- FastAPI server
- Image + text mode
- JSON mode
- Project learning (v0.6.0)
- Offline testing mode

Latest version: **v0.6.0**

## Contents

### Getting Started

- [Installation](installation.md)
- [CLI Usage](cli.md)
- [Python API](python_api.md)

### Core System

- [Architecture Overview](architecture.md)
- [Sessions](sessions.md)
- [RAG System](rag.md)
- [History Management](history.md)
### Advanced Features

- [Response Metadata Schema](metadata_schema.md)

- [JSON response mode](json_mode.md)
- [Token Usage Logging](token_usage.md)
- [Chunk Normalization (Planned)](chunk_normalization.md)
- [Server API](server.md)


### Development

- Project structure
- Running tests
- Coverage reports
- Contributing

## Key Features

- Text generation
- Image + text multimodal input
- RAG with SQLite
- Retry + backoff
- Token logging
- JSON output
- Persistent session chat
- Project-aware RAG (v0.6.0)
- Server mode (FastAPI)
- Syntax-aware code formatter

---

## Quick Install

```bash
pip install multimodal-agent
```
With env key:

```bash
export GOOGLE_API_KEY="your-key-here"
```

### **Roadmap**
- v0.5.x — server features, RAG stability
- v0.6.0 — project learning, project profiles, improved image handling
- v0.7.0 — Flutter extension (code generation + analysis)


## Need help?

Open an issue on GitHub or submit a pull request.
PRs improving docs, tests, or performance are always welcome.
