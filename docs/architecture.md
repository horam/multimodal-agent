# **Architecture Overview**

The Multimodal-Agent project is built as a modular, production-oriented framework around Google Gemini.

Its architecture is designed around four core pillars:

    1.  Unified Agent Core — text, image, and JSON generation

    2.  RAG Memory System — project-aware retrieval with SQLite

    3.  Code Generation Engine — Flutter/Dart widget/screen/model generator

    4.  Developer Tools — CLI, FastAPI server, logging, config, sessions

This document explains how all parts work together.

## High-Level Architecture Diagram

                        +-------------------------+
                        |      CLI (agent)        |
                        +-----------+-------------+
                                    |
                                    v
                        +-------------------------+
                        |    MultiModalAgent      |
                        +-----------+-------------+
                                    |
            +-----------------------+--------------------------+
            |                       |                          |
            v                       v                          v
    +------------------+   +---------------------+   +-----------------------+
    |   Gemini Client  |   |      RAG Store      |   |   Codegen Engine      |
    |  (Text / Image)  |   | (SQLite Embeddings) |   | (Flutter/Dart Gen)    |
    +------------------+   +---------------------+   +-----------------------+
            |                      |                            |
            +-----------+----------+                            |
                        |                                       |
                        v                                       v
            +-------------------------+         +---------------------------+
            |   Prompt Builder Layer  |         |  Prompt Templates (Dart)  |
            +-------------------------+         +---------------------------+

## MultiModalAgent Core

Located in:

```bash
multimodal_agent/core/agent_core.py
```

The agent handles:

✔ Text generation

✔ Image + text multimodal queries

✔ JSON responses

✔ Offline “fake mode” (no API key)

✔ Token usage logging

✔ RAG integration

✔ Session tracking

Internally the agent does:

1.  Build a request

2.  Apply formatting (text or JSON)

3.  Check if RAG is enabled → perform vector search

4.  Call the Gemini API (or fake mode)

5.  Normalize output into AgentResponse

6.  Log metadata + usage

## LLM Client Layer

Wrapper around Google Gemini 2.5 Flash and other models.

Key features:

-   Auto-detect fake mode (missing API key)

-   Retry + exponential backoff

-   Unified ask() and ask_with_image() entrypoints

-   Handles JSON formatting + parsing

-   Created once per CLI invocation

This abstraction ensures your CLI and server run identically regardless of model version.

## Prompt Builder System (New in v0.8.x)

All code-generation prompts are built in:
```bash
multimodal_agent/codegen/prompts/
```

Files:

•   widget_prompt.py

•   screen_prompt.py

•   model_prompt.py

Each exposes a pure function:
```python
def build_widget_prompt(name, stateful=False, description=""):
```

These builders guarantee:


✔ Stable structure

✔ No markdown

✔ No comments

✔ Exact class names

✔ Valid minimal Flutter code

This solves the main problem with LLM-based generation: inconsistent prompt quality.


## Codegen Engine

Located in:
```python
multimodal_agent/codegen/engine.py
```

Responsible for turning user input into actual files:

Responsibilities:

-   Detect Flutter project root

-   Sanitize class names (PascalCase)

-   Convert names to snake_case paths

-   Build LLM prompt

-   Send request to Gemini

-   Validate + clean Dart output

-   Ensure imports (material.dart)

-   Write files (widgets/, screens/, models/)

Validation includes:

-   Must contain exactly one class

-   Class name must match sanitized version

-   No comments or markdown

-   File must be syntactically clean

If the LLM misbehaves → the engine raises a clean error.



## RAG Memory System

Stored in:
```bash
multimodal_agent/rag/
```

Powered by SQLite embeddings, with chunk normalization and tagging.

Supports:

-   Semantic search on conversation memory

-   Project learning (v0.6+)

-   Per-session recall

-   Memory summaries

-   Noise filtering

Typical workflow:

```bash
User → Query → RAG search → Append context → LLM → Store response → Update memory
```

## CLI Architecture

All commands defined in:
```bash
multimodal_agent/cli/cli.py
```

Supported commands:

|   Command                         |   Purpose            |
|-----------------------------------|-----------------------|
|   agent ask "text"                |   Normal text queries |
|   agent image img.png "question"  |    Image + text       |
|   agent chat                      | Interactive session   |
|   agent gen widget FooWidget      |   Code generation     |
|   agent history                   |  Inspect RAG memory   |
|   agent config set-key            |   Configuration       |
|   agent server                    |    Run FastAPI        |   

Each command delegates to specialized handlers for readability + testability.


## Server Architecture

Located in:
```bash
multimodal_agent/server/
```

Built with FastAPI, not Flask.

Endpoints:

-   /ask

-   /ask-image

-   /chat

-   /embed

-   /health

Designed to be:

✔ Production-ready

✔ Stateless (sessions stored in RAG)

✔ Easy to deploy (Docker + Uvicorn)


## Offline Fake Mode (Critical for Tests)

If:
```bash
GOOGLE_API_KEY=""
```

The agent will not call Google — it instead returns:
```bash
FAKE_RESPONSE: `<prompt>`
```

This makes:

-   Unit tests fast
-   Integration tests deterministic
-   CI runs without API keys


## Project Learning System

Added in v0.6.0:

-   Scans a Flutter project
-   Extracts structure, dependencies, files
-   Generates a “project profile”
-   Stores it in RAG for future reasoning

Useful for:

-   Code refactoring suggestions
-   Automated code reviews
-   Project-aware code generation


## Utility Layer

Includes:

-   File I/O
-   Image loading
-   Token tracking
-   Path helpers
-   Sanitization utilities


## Future Expansions (Roadmap)

-   Codegen for:
-   Repositories
-   Services
-   Enums
-   Abstract classes
-   Riverpod providers
-   Feature modules
-   Full Flutter project scaffolding:

```bash
agent gen app my_app
```

-   Code analysis:
```bash
agent analyze lib/
```

-   Dart formatting using dart format hook
