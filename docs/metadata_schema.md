# **Response Metadata Schema**

Every call to the Multimodal Agent returns an **AgentResponse** object containing:

* **text** — the primary output (string)
* data** — parsed JSON (if **response_format="json"**)**
* **usage** — token usage statistics
* **metadata** — optional extended data (future use)
* **raw** — raw model response (only if enabled)

This document defines the schema for these fields.

---

## **AgentResponse Structure**

Python structure:

```
AgentResponse(
    text: str | None,
    data: dict | None,
    usage: dict | None,
    raw: Any | None = None
)
```

JSON-serializable form:

```
{
  "text": "...",
  "data": null,
  "usage": {
    "prompt_tokens": 123,
    "response_tokens": 45,
    "total_tokens": 168
  }
}
```

---

## **Field Definitions**

### **text**

Primary output returned by:

* agent.ask()
* agent.ask_with_image()
* **CLI (**agent ask ...**)**
* Code generation
* Server mode

**Behavior by mode:**

| **Mode** | **text****Value**           |
| -------------- | --------------------------------- |
| Normal         | Model-generated string            |
| JSON mode      | Raw JSON string returned by model |
| Offline mode   | "FAKE_RESPONSE:`<your prompt>`" |
| Image mode     | Description or multimodal output  |

---

###  **data**

Parsed JSON, only populated when:

```
response_format="json"
```

Example:

Input prompt:

```
agent.ask("Return JSON", response_format="json")
```

Response:

```
{
  "text": "{\"message\": \"hi\"}",
  "data": { "message": "hi" }
}
```

**Offline mode behavior:**

**In ** **offline JSON mode** **, **data** is:**

```
None
```

(because fake mode does not generate JSON)

---

### **usage**

Token usage structure:

```
{
  "prompt_tokens": 91,
  "response_tokens": 23,
  "total_tokens": 114
}
```

Always present except in certain test stubs.

See **token_usage.md** for full detail.

---

### **raw (optional)**

Raw model object, when enabled via:

```
agent = MultiModalAgent(return_raw=True)
```

Useful for debugging:

```
print(resp.raw.candidates[0].content)
```

Not returned in CLI or server output unless explicitly enabled.

---

## **Image Metadata Schema**

When using:

```
agent.ask_with_image(prompt, load_image_as_part(path))
```

The final metadata includes:

```
{
  "text": "...",
  "usage": { ... },
  "image": {
    "mime_type": "image/jpeg",
    "size_bytes": 104322,
    "mode": "RGB"
  }
}
```

(Only available when **return_raw=True** or server mode includes metadata.)

---

## **Code Generation Metadata**

For calls such as:

```
agent gen widget HomeScreen
```

The model response internally includes:

```
{
  "text": "<dart code>",
  "usage": { ... },
  "codegen": {
    "class_detected": "HomeScreen",
    "validated": true,
    "output_path": "lib/widgets/home_screen.dart"
  }
}
```

This metadata is currently **not exposed to the user**, but part of internal planning for v0.9.x.

---

##  **RAG Metadata**

When RAG is enabled:

```
agent = MultiModalAgent(enable_rag=True)
```

The internal schema includes:

```
{
  "rag": {
    "enabled": true,
    "retrieved_chunks": 3,
    "tokens_added": 428,
    "session_id": "abc123"
  }
}
```

This metadata is **not shown** unless debugging hooks are activated.

---

## **CLI Metadata**

The CLI prints markdown with metadata sections:

```
### Question
...

### Answer
...

---
type: ask
command: ask
```

No internal fields (like raw model metadata) are shown.

---

## **Server Mode Schema**

The FastAPI server returns:

```
{
  "text": "...",
  "data": null,
  "usage": {
    "prompt_tokens": 88,
    "response_tokens": 31,
    "total_tokens": 119
  }
}
```

Future versions may include:

* latency_ms
* model_name
* **rag** block

---

## **Offline Mode Schema**

When no **GOOGLE_API_KEY** is present:

```
{
  "text": "FAKE_RESPONSE: hello",
  "data": null,
  "usage": {
    "prompt_tokens": 5,
    "response_tokens": 5,
    "total_tokens": 10
  }
}
```

Format is always preserved.

Useful for deterministic test runs.

---

## **Planned Extensions (v0.9.x)**

New metadata fields expected:

* source**: **"text" | "image" | "codegen"
* **latency_ms**: end-to-end latency
* **prompt_preview**: first 200 chars of formatted prompt
* **rag_context_preview**: snippets of retrieved chunks
* **safety_attributes**: Gemini safety metadata
