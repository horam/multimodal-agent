# CLI Usage (`agent`)

The `agent` CLI is the main interface for interacting with the Multimodal-Agent
system. It supports:

- Text queries
- Image + text queries
- Interactive chat
- RAG memory browsing
- Project learning
- Flutter code generation (v0.8.0+)
- Config management
- Running a FastAPI server

# Basic Commands

## Show version

```bash
agent --version
```

**Ask a text question**

```bash
agent ask "What is Flutter?"
```

**JSON mode**

```bash
agent ask "example" --json
```

**Disable RAG for a single query**

```bash
agent ask "hello" --no-rag
```

# Image + Text Queries

```bash
agent image cat.jpg "what is in this image?"
```

Supports --json and --no-rag just like ask.

# Interactive Chat Mode

```bash
agent chat
```

With persistent session ID:

```bash
agent chat --session my-dev-session
```

Disable RAG during chat:

```bash
agent chat --no-rag
```

# Flutter Code Generation (v0.8.0+)

The CLI can generate Flutter boilerplate files:
	•	Widgets → lib/widgets/
	•	Screens → lib/screens/
	•	Models → lib/models/

Run inside a Flutter project (must contain pubspec.yaml).

⸻

**Generate a stateless widget**

```bash
agent gen widget MyWidget
```

**Generate a stateful widget**

```bash
agent gen widget Counter --stateful
```

**Generate a screen**

```bash
agent gen screen HomeScreen
```

**Generate a model**

```bash
agent gen model UserProfile
```

**Overwrite existing file**

```bash
agent gen widget MyWidget --override
```

All names are auto-normalized:

- Class: PascalCase
- File: snake_case.dart

Example:

```bash
agent gen widget UserCard
```

Creates:

```bash
lib/widgets/user_card.dart
```

# History & Memory (RAG)

**Show recent memory**

```bash
agent history show
```

Limit number of rows:

```bash
agent history show --limit 20
```

Hide noise

```bash
agent history show --clean
```

**Delete all memory**

```bash
agent history clear
```

**Summarize memory via LLM**

```bash
agent history summary
```

**Delete specific memory item**

```bash
agent history delete 42
```

# Project Learning (RAG Profiles)

Teach the agent about a project:

```bash
agent learn-project /path/to/project
```

Store with specific ID:

```bash
agent learn-project /app --project-id myapp
```

List learned projects:

```bash
agent list-projects
```

Show project profile:

```bash
agent show-project myapp
```

Inspect without saving:

```bash
agent inspect-project /app
```

# Server Mode (FastAPI)

Run a local API server:

```bash
agent server --port 8000
```

# Config Management

**Set API key**

```bash
agent config set-key YOUR_KEY
```

**Set chat model**

```bash
agent config set-model gemini-2.5-flash
```

**Set image model**

```bash
agent config set-image-model gemini-2.5-flash
```

**Set embedding model**

```bash
agent config set-embed-model text-embedding-004
```

**Show full config**

```bash
agent config show
```

# Offline Fake Mode

If GOOGLE_API_KEY is missing, the agent runs in fake offline mode.

Example:

```bash
agent ask "hello"
```

Output:

```bash
FAKE_RESPONSE: hello
```

Useful for:

- CI environments
- Tests
- No network access

# Debug Logging

Enable verbose logs:

```bash
agent --debug ask "hi"
```

**Summary of Commands**

| Category | Command |
| ---- | ---- |
| Text | agent ask "..."|
|Image	| agent image file.png "..." |
|Chat | agent chat |
| History | agent history show, clear, summary, delete |
|	Learning	|	agent learn-project path	|
|	Codegen		|	agent gen widget/screen/model Name	|
|	Server	|	agent server	|
|	Config	|	agent config ...	|

