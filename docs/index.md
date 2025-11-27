# Multimodal Agent

A lightweight, production-ready wrapper around **Google Gemini** with:

- Multimodal support (text + images)
- Session-based conversational memory
- SQLite-powered RAG vector store
- High test coverage (90%+)
- Robust CLI (`agent`)
- Retry logic + error handling
- Extensible architecture for plugins & tooling

This documentation will guide you through:

## Contents

### Getting Started

- [Installation](installation.md)
- [CLI Usage](cli.md)
- [Python API](python_api.md)

### Core System

- [Architecture Overview](architecture.md)
- [Sessions](sessions.md)
- [RAG Memory](rag.md)
- [History Management](history.md)

### Advanced Features

- [Response Metadata Schema](metadata_schema.md)

- [JSON response mode](json_mode.md)
- [Token Usage Logging](token_usage.md)
- [Chunk Normalization (Planned)](chunk_normalization.md)

### Development

- Project structure
- Running tests
- Coverage reports
- Contributing

## Version Highlights (v0.2.6)

- Added SQLite-backed RAG store
- Added session-based memory
- Added `agent history` commands
- Updated schema for future usage
- New docs for RAG and session management

## Why This Project Exists

This agent sits between **Gemini** and your applications to provide:

- A clean interface
- Safer, predictable behavior
- Local memory without external services
- Debuggable pipelines

## 🚀 Quick Start

Install:

```bash
pip install multimodal-agent
```

Ask a question:

```bash
agent ask "What is recursion?"
```

Start a chat session:

```bash
agent chat --session my_chat
```

Enable verbose metadata:

```bash
agent ask "hello" --verbose
```

## Need help?

Open an issue on GitHub or submit a pull request.
PRs improving docs, tests, or performance are always welcome.
