# **Logging System**

The Multimodal Agent uses a structured and consistent logging framework built around Python’s **logging** module. Logging supports:

* Debugging during development
* Tracking model behavior
* Monitoring RAG interactions
* Inspecting code generation flow (new in v0.8.x)

All logs are routed through the centralized helper:

```
multimodal_agent.logger.get_logger(name)
```

---

# **Log Levels**

The agent respects the environment variable:

```
export LOGLEVEL=DEBUG
```

Or CLI flag:

```
agent --debug
```

### **Supported levels:**

| **Level** | **Description**                                         |
| --------------- | ------------------------------------------------------------- |
| DEBUG           | Verbose internal details (RAG queries, retries, sanitization) |
| INFO            | High-level behavior (initialization, file generation)         |
| WARNING         | Recoverable problems                                          |
| ERROR           | Failures during model calls or generation                     |
| CRITICAL        | Rare, system-level failures                                   |

---

# **Where Logging Occurs**

### **Agent Core (agent_core.py)**

Logs include:

* Agent initialization
* Whether offline fake mode was triggered
* Retry/backoff cycles
* JSON parsing attempts
* RAG lookup status

Example:

```
[INFO] Initializing MultiModal agent...
[DEBUG] No API key found → entering offline FAKE mode.
```

---

### **RAG System (rag_store.py)**

Logs include:

* Writing content to SQLite
* Normalization of chunks
* Loading/merging histories
* Project-profile operations

Example:

```
[DEBUG] Stored chunk id=182 in session=project:app
```

---

### **CLI (cli.py)**

Logs include:

* Command dispatching
* Error messages
* Codegen generation path

Example:

```
[INFO] Widget generated at /lib/widgets/home_screen.dart
```

---

### **Code Generation Engine (codegen/engine.py)**

New in **v0.8.x**, logs capture:

* Sanitized class names
* Prompt construction
* Extraction of code blocks
* Validation failures (missing class name, missing import)

Example:

```
[DEBUG] Expected class: HomeScreen, found in output: True
```

---

# **Enabling Debug Mode**

### **CLI**

```
agent --debug ask "hello"
```

### **Python**

```
import os
os.environ["LOGLEVEL"] = "DEBUG"

agent = MultiModalAgent()
agent.ask("hello")
```

---

# **Offline Mode Logging**

When no API key is provided (**GOOGLE_API_KEY=""**), the agent logs:

```
[DEBUG] Fake-mode active: returning deterministic mock response.
```

Fake-mode logs also suppress unnecessary noise to keep unit-test output clean.

---

# **Logging in Server Mode**

When running:

```
agent server
```

Logging integrates with Uvicorn.

Debug mode can be enabled:

```
agent --debug server
```

Or:

```
export LOGLEVEL=DEBUG
uvicorn ...
```

Server logs include:

* Request metadata
* Inference timing
* Error responses with structured JSON

---

# **Integration Notes**

### **Best practices:**

* Use **DEBUG** during development
* Use **INFO** in production environments
* Avoid writing sensitive content to logs
* For security, RAG text is never logged verbatim unless **DEBUG** is enabled

---

# **Future Improvements**

Logging roadmap:

* Structured logs in JSON format
* Log rotation
* Rich debug dashboard in VS Code extension
* Model latency + token cost analytics
