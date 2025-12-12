# **Usage Logging**

The Multimodal-Agent includes optional **token usage tracking**, which helps you understand:

* How many tokens your prompts consumed
* How many tokens the model responded with
* The total cost of an interaction
* Whether the model ran online or offline

Usage logging is **off by default** to keep the console clean unless you explicitly request it.


## **How Usage Logging Works**

Every response includes an internal **usage** dictionary:

```
{
    "prompt_tokens": 123,
    "response_tokens": 45,
    "total_tokens": 168
}
```

When running through the CLI:

```
agent ask "Hello" --debug
```

The agent prints:

```
[usage] prompt=123 response=45 total=168
```

Debug mode automatically shows usage logging.


## **Offline Mode (Fake Usage)**

When **no API key** is provided:

```
export GOOGLE_API_KEY=""
agent ask "hello"
```

The agent switches to a **fake offline mode**, returning:

* FAKE_RESPONSE: ...
* synthetic token usage values

This is essential for:

* running tests
* CI environments
* developing without spending tokens

Example:

```
AgentResponse(
    text="FAKE_RESPONSE: hello",
    usage={
        "prompt_tokens": 5,
        "response_tokens": 5,
        "total_tokens": 10
    }
)
```

This allows unit tests to assert offline behavior consistently.



## **Usage Logging in Tests**

The test suite includes multiple checks:

### **1. Validate usage values exist**

```
assert result.usage["total_tokens"] > 0
```

### **2. Test offline mode produces FAKE_RESPONSE**

```
monkeypatch.setenv("GOOGLE_API_KEY", "")
result = agent.ask("hello")
assert "FAKE_RESPONSE" in result.text
```

### **3. JSON mode excludes data in offline mode**

```
assert result.data is None
```

---

## **Enabling Usage Logging Programmatically**

Usage logging lives at:

```
agent.usage_logging = True
```

Example:

```
from multimodal_agent import MultiModalAgent

agent = MultiModalAgent()
agent.usage_logging = True

response = agent.ask("hello")
print(response.usage)
```


## **When Usage Logging Is Automatically Suppressed**

Some operations suppress usage logs:

* During code generation (**agent gen widget ...**)
* Inside project learning
* While writing to RAG
* When output is meant to be clean (e.g., pure Dart output)


## **Summary**

| **Feature**       | **Status**                             |
| ----------------------- | -------------------------------------------- |
| Token counting          | ✔️ Fully supported                         |
| Fake usage offline mode | ✔️ Used when API key missing               |
| Automatic logging       | ✔️ via**--debug**                          |
| Programmatic logging    | **✔️ via**agent.usage_logging = True |
| JSON mode compatibility | ✔️ Ensures clean metadata                  |
| Used in tests           | ✔️ Required for consistency                |
