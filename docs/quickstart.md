# Quickstart

Welcome to **Multimodal-Agent** — a lightweight, production-ready wrapper around Google Gemini with RAG, CLI tools, and Flutter code generation.

This guide helps you get running in under a minute.


## Install

```bash
pip install multimodal-agent
```
Set your API key:
```bash
export GOOGLE_API_KEY="your-key-here"
```

No API key?

The library automatically falls back to offline fake mode, returning predictable stub responses for testing and CI.

## Ask Questions (Text)
```bash
agent ask "Explain reactive programming in Flutter"
```

JSON output:
```bash
agent ask "give me a summary" --json
```



## Ask With an Image
```bash
agent image ./photo.png "What is shown in this picture?"
```



## Start Chat Session
```bash
agent chat
```

Chat sessions preserve context automatically unless disabled:
```bash
agent chat --no-rag
```


⸻

## Generate Flutter Code (v0.8.0)

Generate a widget
```bash
agent gen widget CoolWidget
```

Stateful:
```bash
agent gen widget CoolCounter --stateful
```

Generate a screen
```bash
agent gen screen HomeScreen
```

Generate a model
```bash
agent gen model UserProfile
```

Overwrite existing files:
```bash
agent gen widget CardItem --override
```

Files are created inside:
```bash
lib/widgets/
lib/screens/
lib/models/
```

Class names are automatically sanitized (e.g., 123temp → W123temp).


## Use Python API
```python
from multimodal_agent.core.agent_core import MultiModalAgent

agent = MultiModalAgent()

response = agent.ask("Explain what a vector database is.")
print(response.text)
```

With an image:
```python
from multimodal_agent.utils import load_image_as_part

img = load_image_as_part("cat.png")
resp = agent.ask_with_image("Describe this cat", img)
print(resp.text)
```
Offline mode example (no API key):
```python
agent = MultiModalAgent()
resp = agent.ask("hello")
print(resp.text)     # → FAKE_RESPONSE: hello
```

## Inspect RAG Memory

Show stored messages:
```bash
agent history show
```
Clear memory:
```bash
agent history clear
```
Summarize history using the model:
```bash
agent history summary
```

## Run the API Server
```bash
agent server --port 8000
```

The server exposes endpoints for:
	•	text queries
	•	image + text
	•	project learning
	•	metadata inspection


## Learn a Project (Code-Aware RAG)

```bash
agent learn-project ./my_flutter_app
```
This stores a structured project profile in the RAG database.

List stored projects:
```bash
agent list-projects
```


## Next Steps
	•	Explore the CLI reference￼
	•	Learn about Flutter code generation￼
	•	Read the Python API guide￼

⸻

You’re ready to use Multimodal-Agent for code generation, RAG, multimodal chat, and AI-assisted development workflows.
