# History & Memory Management

The CLI includes ergonomic tools for inspecting and managing memory.

Introduced in **v0.2.6**.



# Commands

## Show history

agent history show --limit 20


## Show history for a session

agent history show --session chatA



# Delete a specific chunk
```bash
agent history delete 42
```


# Clear history
```bash
agent history clear
```

or per session:
```bash
agent history clear --session abc
```

# Summaries

```bash
agent history summary --limit 50
```

The agent summarizes recent history using Gemini (RAG disabled for the summary call).



# Under the Hood
- Uses the `SQLiteRAGStore`
- Performs fast range queries via indexed tables
- Deletes cascade into embeddings  