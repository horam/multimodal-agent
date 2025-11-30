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
- 🔹 **Automatic formatting engine (JSON / code / XML / plain)**
- 🔹 **Language detection for Python, JS, Java, Kotlin, Swift, Obj-C, Dart, C++, XML, JSON**

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

RAG Mode (Optional)

You can request structured JSON output by passing `response_format="json"`:

```python
from multimodal_agent import MultiModalAgent

agent = MultiModalAgent(enable_rag=False)

result = agent.ask("Return a JSON object with a and b.", response_format="json")
print(result.data)   # {'a': 1, 'b': 'hello'}
```

The agent automatically:

- Strips ```json fenced blocks
- Parses JSON
- Falls back to {"raw": `<text>`} when invalid JSON is returned
- Maintains identical behavior in online and offline mode

## Offline Mode

If no `GOOGLE_API_KEY` is found, the agent enters **offline simulation mode**:

- No real API calls are made
- Responses are deterministic and prefixed with `"FAKE_RESPONSE:"`
- JSON mode still returns proper `{}`-dicts
- Usage metadata is simulated for testing

This ensures the package is fully testable without credentials.

## AgentResponse Object

All `.ask()` and `.chat()` calls return:

```python
AgentResponse(
    text="<model text>",
    data={...},          # JSON dict if json mode, else None
    usage={
        "prompt_tokens": ...,
        "response_tokens": ...,
        "total_tokens": ...,
    }
)
```

## Asking With Images

```python
from multimodal_agent.utils import load_image_as_part

img = load_image_as_part("photo.jpg")
resp = agent.ask_with_image("Describe this image", img)
print(resp.text)
```

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

### **Formatted output**

<pre class="overflow-visible!" data-start="1928" data-end="1974"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent ask "write python </span><span>code</span><span>" </span><span>--format</span><span>
</span></span></code></div></div></pre>

Produces fenced, language-annotated code.

## Token Usage Logging (v0.3.2)

Multimodal-Agent can automatically record token usage for every request (text, JSON, or image-based).

Usage logging is **enabled by default**.

Each call writes a compact entry into:
```bash
~/.multimodal_agent/usage.log
```

### Example Log Entry
2025-01-12T15:22:14Z | model=gemini-2.5-flash | prompt=42 | response=18 | total=60

### Disable Usage Logging

If you do not want any local logging:

```python
agent = MultiModalAgent(enable_rag=False)
agent.usage_logging = False
```

**Custom Log Path**

```python
agent.usage_log_path = "/path/to/your/custom.log"
```

**JSON + Image Mode Support**
Usage logging works seamlessly across:


- ask()
- ask_with_image()
- response_format="json"
- offline FakeResponse mode

Logging is  **silent** , non-blocking, and wrapped in safe try/except guards.

It never interferes with the agent and never breaks tests.

## **Formatting Engine (v0.4.0)**

Multimodal-Agent now includes a robust formatter that automatically detects and beautifies output.

Supported types:

* **JSON** → pretty-printed, stable formatting
* **Code** → wrapped in triple backticks with detected language
* **XML / HTML** → pretty printed
* **Plain text** → normalized

### Usage:

<pre class="overflow-visible!" data-start="1133" data-end="1217"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>resp = agent.ask(</span><span>"write python code"</span><span>, formatted=</span><span>True</span><span>)
</span><span>print</span><span>(resp.text)
</span></span></code></div></div></pre>

Example output:

<pre class="overflow-visible!" data-start="1236" data-end="1299"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-markdown"><span><span>```python
def add(a, b):
    return a + b
```</span></span></code></div></div></pre>

## **Language Detection (v0.4.0)**

The formatter uses the internal `detect_language()` to identify code automatically.

Detected languages include:

* Python
* JavaScript
* Java
* Kotlin
* Swift
* Objective-C
* Dart
* C++
* JSON
* XML/HTML
* Plain text

### Example:

<pre class="overflow-visible!" data-start="1696" data-end="1828"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent.formatting </span><span>import</span><span> detect_language

</span><span>print</span><span>(detect_language(</span><span>"fun greet(name: String)"</span><span>))  </span><span># → kotlin</span></span></code></div></div></pre>

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

v0.3.2 — Token usage logging

v0.4.0 — Formatting engine + language detection

v0.5.0 — Agent server mode

v0.6.0 — VS Code extension

v1.0.0 — Website + demos + documentation

# License

MIT License.
