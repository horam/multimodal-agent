# Multimodal-Agent

A lightweight, production-ready wrapper around **Google Gemini** offering:

- A powerful CLI (`agent`)
- Code generation for Flutter (widgets, screens, models)
- RAG memory with SQLite
- FastAPI server mode
- Image + text multimodal queries
- JSON output mode
- Project learning & analysis
- Offline / fake-response mode for testing
- Clean usage logging & retry/backoff
- Syntax-aware output formatting

Latest version: **v0.8.0**

---

## Contents

### Getting Started
- [Installation](installation.md)
- [Quickstart](quickstart.md)
- [CLI Usage](cli.md)
- [Python API](python_api.md)

### Core System
- [Architecture Overview](architecture.md)
- [Sessions](sessions.md)
- [RAG System](rag.md)
- [History Management](history.md)
- [Configuration](config.md)

### Code Generation (v0.8.0)
- [Flutter Codegen Overview](codegen_overview.md)
- [Widget / Screen / Model Generation](codegen_flutter.md)

### Advanced Features
- [Response Metadata Schema](metadata_schema.md)
- [JSON Response Mode](json_mode.md)
- [Token Usage Logging](token_usage.md)
- [Usage Logging Behavior](usage_logging.md)
- [Server API](server.md)

---

## Key Features

- Text generation
- Image + text multimodal input
- Local RAG using SQLite
- Project-aware learning & analysis
- Interactive chat sessions
- Token accounting & logging
- Offline fake-mode for deterministic tests
- Syntax-aware code formatting
- Flutter code generation:
  - `agent gen widget`
  - `agent gen screen`
  - `agent gen model`

---

## Quick Install

```bash
pip install multimodal-agent
```
Set your API key:
```bash
export GOOGLE_API_KEY="your-api-key"
```
No key?
The CLI and Python API still work in **offline fake mode**, returning predictable response for testing.

# need help?
Open an issue on Github or submit a pull request.
Contribution to docs, tests, and performance improvements are always welcome.