
# Agent Overview

The Multimodal Agent is the core high-level interface for interacting with Google Gemini.
It supports text, image+text questions, JSON responses, RAG-enhanced conversations, and offline fake-mode for deterministic testing.

This document explains how the agent works and how to use it programmatically.


## Importing the Agent
```python
from multimodal_agent.core.agent_core import MultiModalAgent
```

Create an agent instance:
```python
agent = MultiModalAgent(
    model="gemini-2.5-flash",
    enable_rag=True,   # enables SQLite RAG memory
)
```

If no API key is found in environment variables, offline fake-mode is activated automatically.


## Basic Text Generation
```python
response = agent.ask("Explain flutter widgets.")
print(response.text)
```

**Returned object: AgentResponse**

```python
AgentResponse(
    text="...", 
    data=None, 
    usage={"prompt_tokens": ..., "response_tokens": ..., "total_tokens": ...}
)
```


## Image + Text Questions
```python
from multimodal_agent.utils import load_image_as_part

image = load_image_as_part("cat.png")
response = agent.ask_with_image("Describe the image", image)
print(response.text)
```
Supports:
-	JPG / PNG
-	Multiple images (if model supports it)


## JSON Mode

The agent can force the model to produce strict JSON:
```python
response = agent.ask(
    "Give me a summary with fields title and score",
    response_format="json",
)
print(response.data)
```

Output example:
```json
{
  "title": "Summary",
  "score": 9
}
```

If JSON parsing fails, an AgentError is raised.


## Offline Fake Mode (for Tests)

If you run the agent without an API key:
```bash
export GOOGLE_API_KEY=""
```

Or you omit it entirely, the agent switches to fake mode.

Behavior:

|   Input   |	Output    |
|-----------|-------------|
|agent.ask("hello")	    |   Returns FAKE_RESPONSE: hello    |
|agent.ask("hello",response_format="json")  |	Returns JSON encoded fake response| 
|Token usage	        |   Deterministic stub values   |

This makes CI / unit tests stable and zero-cost.


## RAG Memory System

When enable_rag=True, the agent maintains a memory buffer in SQLite.
```python
agent = MultiModalAgent(enable_rag=True)
agent.ask("What is object-oriented programming?")
```
Behind the scenes:
	1.	User query → embedded
	2.	Similar chunks retrieved from SQLite
	3.	Prompts are augmented with retrieved context
	4.	Output is saved back into memory

To inspect memory:
```bash
agent history show --limit 20
```

## Sessions

You may group interactions under a session:
```python
agent.ask("Start a new conversation", session_id="research1")
agent.ask("Add more context", session_id="research1") 
```

From CLI:
```bash
agent ask "Hello" --session my_session
```

## Token Usage Tracking

Every response includes a .usage field:
```python
print(response.usage)
```

Example:
```python
{
  "prompt_tokens": 123,
  "response_tokens": 45,
  "total_tokens": 168
}
```

Useful for monitoring cost.


## Error Handling

All agent-related errors raise clean subclasses of AgentError:
-	Invalid JSON output
-	API failures
-	Timeout
-	Missing image
-	RAG store issues
```python
from multimodal_agent.errors import AgentError

try:
    agent.ask("...")
except AgentError as e:
    print("Agent failed:", e)
```


## Using Custom Models
```python
agent = MultiModalAgent(model="gemini-pro")
```

From CLI:
```bash
agent --model gemini-pro ask "Hello"
```

## Integration with Code Generation Engine

The agent itself is independent from codegen, but the CLI uses both:
```bash
agent gen widget HomeScreen
```

This internally:
1.	Builds a codegen prompt
2.	Sends it to the agent
3.	Validates output
4.	Writes the .dart file

## Full Example
```python
from multimodal_agent.core.agent_core import MultiModalAgent

agent = MultiModalAgent(enable_rag=True)

response = agent.ask("Explain Riverpod in Flutter.")
print("Answer:", response.text)
print("Tokens:", response.usage)
```

## When to Use the Agent Programmatically

Use the agent directly if you need:
-	Embedding your app with Gemini
-	Multimodal Q&A
-	RAG-powered assistants
-	JSON-producing agents
-	Offline test-safe inference

Use CLI if you want:
-	Quick questions
-	Code generation
-	Server hosting
-	Memory debugging

## Summary

|   Feature     |	Supported   |
|---------------|---------------|
|   Text + Image  |     ✔       |
|   JSON output	  |     ✔       |
|   Offline fake mode | 	✔   |
|   RAG memory	|       ✔       |
|   Sessions	|       ✔       |
|   Token usage	|       ✔       |
|   Project learning    |	✔   |
|   Code generation engine | ✔  |

