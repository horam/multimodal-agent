# **Sessions**

Sessions allow the Multimodal-Agent to maintain **context across multiple interactions**.

Each session has its own memory stream, enabling:

* Multi-turn conversations
* Independent threads of reasoning
* Separate RAG histories
* Clean isolation between tasks or projects


## **How Sessions Work**

Every interaction with the agent can be associated with a **session ID**:

```
agent ask "Explain caching layers" --session study
```

The same session ID can be used repeatedly:

```
agent ask "Continue" --session study
```

This lets the agent retrieve context from the RAG memory associated with that session.



## **Why Sessions Matter**

| **Feature**       | **Description**                                                  |
| ----------------------- | ---------------------------------------------------------------------- |
| Persistent conversation | The agent remembers user messages and responses.                       |
| Contextual RAG          | Retrieval is limited to entries from the same session (unless forced). |
| Multi-session workflows | You can maintain several “workspaces” of knowledge.                  |
| Better isolation        | Different projects or topics never interfere with each other.          |



## **Session IDs in CLI Commands**

### **Ask command**

```
agent ask "Hello" --session chat1
```

### **Image command**

```
agent image pic.png "Describe this" --session design_experiment
```

### **Chat mode (interactive)**

```
agent chat --session daily
```

The session continues until you exit chat mode.


## **How Sessions Interact with RAG Memory**

Each message added to the RAG store is tagged with:

* session_id
* **role (**user**, **assistant**, or **project_profile**)**
* timestamp
* **source (**ask**, **chat**, **project-learning**, etc.)**

Example RAG record:

```
{
  "session_id": "study",
  "content": "Explain transformers...",
  "role": "user",
  "source": "ask"
}
```

When the agent receives a query:

1. It looks for relevant RAG entries **only within the same session**
2. Applies vector similarity
3. Constructs a retrieval-augmented prompt
4. Produces a contextual answer

Disable RAG for stateless interactions:

```
agent ask "hello" --no-rag
```


## **Offline Mode (No API Key)**

If no **GOOGLE_API_KEY** is found:

* Sessions still work
* RAG still stores and retrieves memory
* The model returns deterministic **FAKE_RESPONSE:** answers
* No external API calls are made

This is ideal for:

* testing
* CI pipelines
* working offline

Example:

```
agent ask "hello" --session test
```

Produces:

```
FAKE_RESPONSE: hello
```


## **Managing Session Memory**

### **View recent history**

```
agent history show --session study
```

### **View only last N items**

```
agent history show --limit 20 --session study
```

### **Show cleaned history (no FAKE_RESPONSE, no system noise)**

```
agent history show --clean --session study
```

### **Clear all memory**

```
agent history clear
```

### **Delete a specific entry**

```
agent history delete 42
```


## **Recommended Session Naming Conventions**

Use short, descriptive names:

* flutter_app
* thesis
* design_review
* bugfix_123
* morning_chat

Avoid:

* very long names
* names with spaces
* names used for unrelated topics



## **Quick Examples**

### **Math session**

```
agent ask "What is Fourier transform?" --session math
agent ask "Give me an example" --session math
```

### **Flutter session**

```
agent ask "How do I use Navigator 2.0?" --session flutter
```

### **Debug session**

```
agent chat --session debug_issue
```



## **Summary**

| **Feature**                     | **Status**        |
| ------------------------------------- | ----------------------- |
| Persistent chat history               | ✔️                    |
| Session-scoped RAG retrieval          | ✔️                    |
| Isolated memory streams               | ✔️                    |
| Works offline                         | ✔️ FAKE_RESPONSE mode |
| Fully supported across ask/image/chat | ✔️                    |
| CLI + API support                     | ✔️                    |
