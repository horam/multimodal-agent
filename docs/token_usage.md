# **Token Usage Logging**

The Multimodal Agent automatically tracks token usage for:

* Text-only generation
* Image + text multimodal generation
* JSON mode
* Offline FAKE mode

Every response—CLI, Python API, or Server—includes a standardized **usage** dictionary.

---

## **What Is Logged?**

Every model call (real or offline) returns:

```
{
  "prompt_tokens": <int>,
  "response_tokens": <int>,
  "total_tokens": <int>
}
```

These values appear under:

```
response.usage
```

Example (Python):

```
resp = agent.ask("Hello")
print(resp.usage)
```

Output:

```
{ "prompt_tokens": 5, "response_tokens": 12, "total_tokens": 17 }
```

---

## **Logging in Online Mode**

When a real model is used, the agent extracts token usage from the Gemini API response.

Example server output:

```
{
  "text": "Hello!",
  "usage": {
    "prompt_tokens": 7,
    "response_tokens": 4,
    "total_tokens": 11
  }
}
```

---

## **Logging in Offline Fake Mode**

If no API key is set:

```
export GOOGLE_API_KEY=""
```

Then responses are generated deterministically, and token usage is simulated:

Example:

```
{
  "text": "FAKE_RESPONSE: test",
  "usage": {
    "prompt_tokens": 4,
    "response_tokens": 5,
    "total_tokens": 9
  }
}
```

This ensures:

✔ CI tests remain stable

✔ No API cost

✔ CLI, server, and Python API behave identically

---

## **CLI Usage Logging**

Use:

```
agent ask "hello" --debug
```

Output includes:

```
[usage] prompt=5 response=12 total=17
```

---

## **Server Usage Logging**

All server responses include token usage:

```
{
  "text": "...",
  "usage": {
    "prompt_tokens": 11,
    "response_tokens": 18,
    "total_tokens": 29
  }
}
```

This allows frontends (Flutter, React, etc.) to track cost in real time.

---

## **Python API Usage Logging**

```
resp = agent.ask("Explain gravity")
print(resp.usage["total_tokens"])
```

Works exactly the same for:

* agent.ask_with_image()
* JSON mode
* Offline mode

---

## **Where Usage Is Stored**

Token usage is *not* persisted in the RAG memory database.

It is only returned per-response.

---

## **Future Extensions (v0.9.x)**

Planned improvements:

* Usage logging per-session
* Cost estimation (USD)
* Project-level usage breakdown
* Heatmap of RAG vs direct model calls

---

## **Summary**

Token usage logging is:

✔ Always included

✔ Consistent across all modes

✔ Deterministic in offline mode

✔ Available in CLI, Server, and Python API

---

If you want, I can update **chunk_normalization.md** next, or skip planned features and continue with **config.md**, **sessions.md**, or anything you choose.

Just say **“next”**.
