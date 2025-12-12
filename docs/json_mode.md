# JSON Mode (response_format="json")

The Multimodal Agent supports strict JSON responses using either:
-	the Python API, or
-	the CLI flag --json

JSON mode ensures that structured outputs are:
-	Valid JSON (strictly parseable)
-	Returned through AgentResponse.data
-	Mirrored as a JSON string in AgentResponse.text

This is strongly recommended for tool output, structured reasoning, and integration workflows.


## Enabling JSON Mode

### Python API
```python
from multimodal_agent.core.agent_core import MultiModalAgent
agent = MultiModalAgent()

result = agent.ask("Give me a JSON object", response_format="json")
print(result.data)
```
Result Structure
```python
AgentResponse(
    text='{"weather":"sunny"}',
    data={"weather": "sunny"},
    usage={...}
)
```

-	**text:** raw JSON string returned by the model
-	**data:** parsed Python dictionary
-	**usage:** token usage metadata


### CLI Mode
```bash
agent ask "Describe your system as JSON" --json
```

Output Example
```json
{
  "weather": "sunny",
  "temperature": 28
}
```



## JSON Mode in Offline Fake Mode

If no API key is set, the agent enters fake mode:
```bash
export GOOGLE_API_KEY=""
```

In fake mode:

**Request**
```python
agent.ask("hello", response_format="json")
```

**Output**
```python
AgentResponse(
    text='{"message": "hello"}',
    data={"message": "hello"},
)
```

Important change in v0.8.x:

✔ **data is now a dict**, not None

✔ JSON behavior is consistent in online/offline mode

✔ Tests expect .data to contain the parsed JSON

This simplifies testing and keeps the model behavior stable.


## Behavior Guarantees

**✔ Always returns valid JSON**

The agent will retry, repair, and normalize the model output.

**✔ No markdown or prose allowed**

Prompts automatically enforce:
```bash
Output ONLY valid JSON. No commentary.
```

**✔ If JSON cannot be parsed → raises AgentError**

Example:
```bash
AgentError: Failed to parse JSON output:
<raw model output>
```



## Common Use Cases

### Structured Information Extraction
```python
agent.ask(
    "Extract name and age.",
    response_format="json"
)
```
```bash
{"name": "Alice", "age": 32}
```
---

### Tool Invocation & Function Arguments

JSON mode allows the agent to be used as a semantic parser.

---

### Integration With Frontend / Mobile Apps

Dart, React, and Flutter consumers benefit from predictable structured output:
```bash
{"title": "Hello", "count": 3}
```


## Error Handling

**Invalid JSON**

If the model returns malformed JSON:
```bash
AgentError: Failed to parse JSON output
```

**Offline Fake Mode Always Succeeds**

Guaranteed output:
```json
{"message": "your_prompt_here"}
```

Useful for:
-	CI pipelines
-	Local unit tests
-	Environments without internet

⸻

## Accessing JSON Results

**Python API**
```python
data = result.data     # dict
raw = result.text      # JSON string
```
**CLI**

Output is printed as clean JSON:
```bash
agent ask "hi" --json
```


## Best Practices

**✔ Always validate required fields:**
```python
if "name" not in result.data:
    raise ValueError("Missing required field: name")
```
**✔ Design prompts like this:**
```bash
Return ONLY valid JSON with fields: name, age, city.
```

**✔ Avoid natural language in JSON mode prompts.**

**✔ For complex schemas, include a template:**
```bash
Provide JSON with this structure:
{
  "title": "",
  "items": []
}
```


## Summary Table

| Mode	|   text    |	data    |
|-------|-----------|-----------|
| JSON mode (online)	|   Raw JSON    |	Parsed dict |
| JSON mode (offline/fake)  |	JSON string	|   Parsed dict |
| Text mode	|   Text/string |   	None    |
