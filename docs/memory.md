# Memory System

The agent stores conversation turns in:

`~/.multimodal_agent/history.json`

---

### Format:

```json
[
  "USER: hello",
  "AGENT: hi!",
  ...
]
```
---
### Functions
* `load_memory()`

* `save_memory(list)`

* `append_memory(entry)`

* `delete_memory_index(i)`

* `reset_memory()`

* `summarize_memory()`

Memory is plain JSON — easy to inspect and portable.
