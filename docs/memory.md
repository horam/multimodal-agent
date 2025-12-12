# **Memory System (RAG Memory)**

The **memory system** is a lightweight Retrieval-Augmented-Generation (RAG) layer built on top of a persistent **SQLite database**.

Every interaction with the agent can be stored, retrieved, summarized, or cleared.

Memory is used by the agent to:

* **Maintain ****context across conversations**
* Retrieve relevant past answers
* **Store ****project profiles** (via agent learn-project**)**
* Improve long chats without sending long prompts
* Provide stable behavior between CLI calls and sessions


## **Overview**

The memory system has three core components:

### **SQLiteRAGStore**

A simple, fast, file-based persistence layer located at:

```
~/.multimodal_agent/memory.db
```

Controls:

* Insert memory chunks
* Query by session
* Query by semantic search (planned)
* Store project profiles
* Clear or delete entries


### **Memory Chunk Format**

Each memory entry is saved with the following schema:

| **Column** | **Description**                                                                |
| ---------------- | ------------------------------------------------------------------------------------ |
| id               | Unique identifier                                                                    |
| content          | Raw text stored                                                                      |
| role             | "user"**,**"assistant"**,**"system"**,**"project_profile"          |
| session_id       | Logical session grouping                                                             |
| created_at       | Timestamp                                                                            |
| source           | "chat"**,**"ask"**,**"project-learning"**,**"test"**, etc.** |

Example JSON block stored inside the chunk:

```
{
  "type": "message",
  "content": "How do I format code?",
  "role": "user"
}
```

---

### **Integration with the Agent**

Memory is automatically used in:

* agent chat
* **agent ask**  *(unless * *--no-rag** used)*
* **Project learning (**agent learn-project**)**

When enabled, the agent retrieves the **most recent and clean** memory chunks and includes them before generating a response.


## **How Memory Is Used During a Query**

### **User makes request**

→ The agent checks whether RAG is enabled.

### **If enabled**

→ Retrieves the most relevant recent memory chunks.

→ Adds them to the model input.

### **After producing an answer**

→ The agent stores the interaction:

```
role=user   → content=prompt
role=assistant → text=response
```

### **Memory grows over time**

The agent becomes context-aware across sessions and CLI calls.


## **Session-Based Memory**

Every interaction can be associated with a **session ID**:

```
agent chat --session my-app
agent ask "Hello" --session design-docs
```

If no session is given:

* **agent ask** uses a **stateless ephemeral session**
* **agent chat** creates or resumes a session automatically

This avoids cross-contamination between unrelated tasks.


## **Managing Memory**

The CLI provides several tools:


### **Show Memory**

```
agent history show
```

Options:

```
--limit 100
--session my-session
--clean          # hides noise: FAKE_RESPONSE, tests, profiles
```

---

### **Clear All Memory**

```
agent history clear
```

This wipes **all** memory chunks from the SQLite database.

---

### **Delete a Specific Chunk**

```
agent history delete <chunk_id>
```

---

### **Summarize Memory**

Uses the model to summarize stored chunks:

```
agent history summary --limit 200
```



## **Project Learning Memory**

When you run:

```
agent learn-project /path/to/project
```

The tool generates a **project profile** containing:

* package name
* directories
* file types
* dependencies
* source file summaries
* semantic markers

This profile is stored in memory using:

```
role = "project_profile"
source = "project-learning"
session_id = "project:<package_name>"
```

You can list stored projects:

```
agent list-projects
```

And inspect one:

```
agent show-project my-project-id
```


## **Offline Mode Interaction**

If **GOOGLE_API_KEY** is missing:

* **the model generates a ****deterministic FAKE_RESPONSE**
* **memory ****still works**
* no network calls occur

This makes offline testing easy.

Memory chunk example in offline mode:

```
{
  "type": "message",
  "content": "FAKE_RESPONSE: test",
  "role": "assistant"
}
```



## **Memory File Location**

On macOS/Linux:

```
~/.multimodal_agent/memory.db
```

On Windows:

```
%USERPROFILE%\.multimodal_agent\memory.db
```

You can override path via environment variable:

```
export MULTIMODAL_AGENT_DB=/custom/path/agent.db
```


## **Best Practices**

### **Use sessions for large or long-term tasks**

```
agent chat --session flutter-app
```

### **Clear memory when switching topics**

```
agent history clear
```

### **Use project profiles for codebases**

```
agent learn-project ./my_flutter_app
```

### **Use** **--no-rag for pure LLM answers**

```
agent ask "What is 2+2?" --no-rag
```
