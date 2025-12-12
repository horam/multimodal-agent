# **RAG System (Retrieval-Augmented Generation)**

The **RAG layer** in **multimodal-agent** is designed to be:

* **Simple** (SQLite-based)
* **Fast** (local only, no vector DB required)
* **Deterministic** (in tests + offline mode)
* **Compatible** with Chat, Ask, Image, and Project Learning flows
* **Optional** (disable via **--no-rag**)

RAG helps the agent remember previous interactions, retrieve useful context, and apply project awareness without re-sending long conversation histories to the model.


## **Purpose of RAG**

RAG is used for:

### **✔ Injecting memory into prompts**

The agent automatically retrieves recent memory entries and sends them along with your question.

### **✔ Improving multi-step workflows**

Long chats can build up relevant context over time.

### **✔ Project-level learning**

Using:

```
agent learn-project /path/to/project
```

the agent builds a project profile and stores it as a RAG memory block, enabling smarter code analysis and contextual follow-up questions.

### **✔ Reducing prompt size**

The model only receives the *recent and relevant* memory entries, not full histories.



## **RAG Architecture Overview**

RAG consists of three main components:



### **SQLiteRAGStore**

The persistence layer storing all memory:

```
~/.multimodal_agent/memory.db
```

It supports:

* add memory chunks
* list memory chunks
* retrieve by session
* store project profiles
* delete individual chunks
* clear entire memory

There is currently **no vector search** — memory is chronological and relevance-based by session and context.

---

### **Memory Chunk Normalization(lightweight)**

Every memory entry is processed as:

```
{
  "type": "message",
  "role": "user" | "assistant" | "project_profile",
  "content": "...",
  "session_id": "some-session",
  "source": "chat" | "ask" | "project-learning" | "test"
}
```

Normalization ensures the agent can use memory consistently regardless of input type.

---

### **RAG Injection Layer**

When you call:

```
agent ask "Explain this code"
```

or

```
agent chat
```

The agent:

1. Loads recent memory (based on session)
2. Filters noise (test content, FAKE_RESPONSE entries, etc.)
3. Produces a context block like:

```
Previous messages:
[user] How do I initialize a Flutter widget?
[assistant] Use const constructors whenever possible.

Current message:
"Explain this code"
```

4. Sends it to the model.

This makes the agent behave like a persistent chat assistant across CLI calls.


## **Enabling / Disabling RAG**

### **RAG ON (default)**

```
agent ask "hello"
```

### **Disable RAG**

```
agent ask "hello" --no-rag
```

This completely bypasses memory injection.

---

## **Memory + RAG in Chat Mode**

Running:

```
agent chat --session demo
```

Starts an interactive session that:

* loads previous memory for session **demo**
* appends new interactions to memory
* retrieves them in future calls

You can resume that chat later:

```
agent chat --session demo
```

---

## **How RAG Works With Project Learning**

When you run:

```
agent learn-project my_app/
```

The system:

1. Scans the entire project directory
2. Builds a structured project profile
3. Stores it as RAG memory:

```
role = project_profile
session_id = "project:<package_name>"
source = project-learning
```

You can inspect stored projects:

```
agent list-projects
```

Or retrieve a profile:

```
agent show-project my_project
```

During code generation (**agent gen widget** / **screen** / **model**), this project knowledge is used IF the agent is model-driven (not stubbed in tests).

---

## **RAG in Offline Mode**

When **GOOGLE_API_KEY** is missing:

* The agent enters **offline fake mode**
* RAG memory still works
* Model returns deterministic **FAKE_RESPONSE**

This allows full offline testing of the RAG subsystem.

Example stored chunk:

```
{
  "role": "assistant",
  "content": "FAKE_RESPONSE: test",
  "source": "ask"
}
```


## **Database Location**

Default path:

```
~/.multimodal_agent/memory.db
```

Override it:

```
export MULTIMODAL_AGENT_DB=/custom/path/memory.db
```


## **Planned Enhancements (v0.9+)**

- Vector search (Lite model)

-   Relevance scoring instead of chronological retrieval

-   Project-level embeddings

-   Query-aware memory selection


## **Summary**

| **Feature**              | **Status** |
| ------------------------------ | ---------------- |
| Persistent memory              | ✔               |
| Session-based retrieval        | ✔               |
| Project profile memory         | ✔               |
| Offline mode support           | ✔               |
| Noise cleaning                 | ✔               |
| Vector search                  | ✘*(planned)*  |
| Metadata-based query filtering | ✘*(planned)*  |
