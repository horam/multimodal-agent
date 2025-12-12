# Error Handling

The Multimodal Agent uses a unified error model based on the AgentError class.
All user-facing errors are clean, predictable, and safe to catch.

This document explains:
-	What errors the system raises
-	When they occur
-	How to handle them
-	How errors differ between online mode and offline fake mode


## Base Error Class

All agent errors inherit from:
```python
from multimodal_agent.errors import AgentError
```

You can catch all domain-specific exceptions via:
```python
try:
    agent.ask("Hello")
except AgentError as e:
    print("Agent failed:", e)
```
This ensures your application never receives raw API exceptions.


## Types of Errors

The following are common error categories.

### JSON Parsing Errors
---

Raised when the model does not return valid JSON:
```python
result = agent.ask("Give JSON", response_format="json")
```
If the model returns invalid JSON, you get:
```bash
AgentError: Failed to parse JSON output
```

Fix:

Improve prompt constraints or reduce creativity; JSON mode requires strict formatting.



### Code Generation Validation Errors
---
When using the CLI:
```bash
agent gen widget HomeScreen
```

The system validates that the generated code:
-	Contains the expected class
-	Has no Markdown
-	Starts with imports/class definitions

If validation fails, you’ll see:
```bash
ValueError: Generated code does not contain class `HomeScreen`.
```

This typically means the LLM was too creative. The built-in prompts are designed to reduce this.

⸻

### Project Root & File System Errors

If a Flutter project root is not detected:
```bash
FileNotFoundError: Could not find pubspec.yaml in any parent directory.
```

Fix: Run agent gen inside a Flutter project or provide a valid path.

⸻

### Offline Fake Mode Errors

When no API key exists (GOOGLE_API_KEY=""), the agent switches to fake mode, which:
-	Never calls external APIs
-	Returns deterministic stub responses
-	Never raises network or API errors

Example fake response:
```python
FAKE_RESPONSE: hello
```

JSON mode produces:
```json
{"message": "hello"}
```

Useful for CI, unit tests, and offline work.

---

### Image Errors

When reading images:
```bash
Error: could not load image.
```

This appears if the file is missing or unreadable.
The CLI logs details but prints a friendly error.

⸻

### RAG Store Errors

SQLite-based RAG may raise:
-	Database locked
-	Invalid chunk
-	Corrupt DB file

The CLI prints helpful guidance:
```bash
Error: RAG storage failure. Try resetting the database.
```

The DB path can be reset by deleting:
```bash
rm -f ~/.multimodal_agent/memory.db
```


---

### Server Errors

Running:
```bash
agent server
```

Common issues:

| Error              |   	Meaning          |
|--------------------|-----------------------|
| Port in use    |	Try another port with --port |
| Missing models  |	Ensure config is correct        |
| Startup timeout |	Slow environment or blocked port |



## Logging and Debug Mode

Set debug mode:
```bash
agent --debug ask "Hello"
```

This prints:
-	Internal exceptions
-	Prompt size
-	Token usage details
-	RAG retrievals

Useful for diagnosing pipeline issues.


## Best Practices for Error Handling

### **Always wrap external calls**
```python
try:
    response = agent.ask("Hello")
except AgentError as e:
    log.error(f"Agent failed: {e}")
```
### **Validate JSON before using it**
```python
data = response.data
if not data:
    raise ValueError("Model returned empty JSON payload")
```
### **Validate codegen output when using the library programmatically**
```python
code = agent.ask(prompt).text
if "class " not in code:
    raise AgentError("Invalid Dart code")

```
## Expected Behavior Summary

|   Scenario |	Behavior   |
|------------|-------------|
|   Missing API key	| Fake-mode, no exceptions    |
|   Invalid JSON	|   AgentError  |
|   Missing image	|   User-friendly error message |
|   Codegen class mismatch  |   	ValueError  |
|   RAG DB issues	|   AgentError  |
|   Model API failure	|   Wrapped in AgentError   |
|   CLI misuse	|   Argparse prints help    |


## Raising Custom Errors

You can raise agent errors manually:
```python
from multimodal_agent.errors import AgentError

raise AgentError("Something went wrong")
```


## When to Report an Issue

Open a GitHub issue if you see:
-	Inconsistent validation behavior
-	Unexpected offline-mode behavior
-	CLI silently failing
-	RAG memory corruption
-	Codegen hallucinations beyond prompt constraints
