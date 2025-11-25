# Response Metadata Schema

The CLI supports two response formats:

- **Minimal mode (default)**  
- **Verbose mode (`--verbose`)**

This keeps the UX clean while allowing programmatic access to details.


# Minimal Schema (default)

```json
{
  "text": "Hello!",
  "image": null
}
```
Purpose:

- Clean CLI output

- Human-friendly

- Great for normal usage

# Verbose Schema (--verbose)

```json
{
  "text": "Hello!",
  "meta": {
    "model": "gemini-2.5-flash",
    "tokens": {
      "prompt": 128,
      "completion": 42,
      "total": 170
    },
    "latency_ms": 89,
    "rag": {
      "chunks_used": [
        { "id": 3, "score": 0.92 },
        { "id": 8, "score": 0.88 }
      ]
    }
  }
}
```
Includes:

-   Model name

-   Token usage

-   Latency


## RAG chunk retrieval info

Recommendation

Default = minimal

Power users = add --verbose
