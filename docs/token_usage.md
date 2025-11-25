# Token Usage Logging (Planned)

Token accounting is crucial for:
- cost tracking
- optimization
- debugging latency
- improving your extension/tooling

---

# CLI Support

When using:

```bash
agent ask "hello" --verbose
```


You will see:

```json
"tokens": {
  "prompt": 54,
  "completion": 18,
  "total": 72
}
```
# Application Usage
You can capture token usage in:

- extensions

- Web integrations

- Server logs (API wrappers)

- Performance dashboards