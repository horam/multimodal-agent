# History Management

The Multimodal-Agent includes a built-in **RAG memory system** backed by SQLite.
All queries can optionally write messages to memory, and you can inspect, filter, or
clear history directly from the CLI.

History is grouped by **session IDs**.  
If you do not provide a session ID, the agent uses a default session.


## Viewing History

Show recent memory entries:

```bash
agent history show
```

Limit the number of entries:
```bash
agent history show --limit 20
```
Filter by session:
```bash
agent history show --session my-app
```

Hide noisy internal messages (FAKE_RESPONSE, project profiles, tests):

```bash
agent history show --clean
```

## Clearing History

Clear all entries:
```bash
agent history clear
```
Clear entries for a specific session:
```bash
agent history clear --session my-app
```


## Deleting a Specific Chunk

Each memory item has a numeric ID.
To delete one:
```bash
agent history delete 42
```


## Summarizing Memory

The agent can summarize memory using the current chat model:
```bash
agent history summary --limit 50
```

Or for a specific session:
```bash
agent history summary --session my-app
```
The summary is generated using AI but is never stored automatically—you’re in control.


## How History Works Internally
-	History is stored inside a SQLite database:
```bash
~/.multimodal_agent/memory.db
```

- Each message is stored with:

    -   content
	-	role (“user”, “assistant”, “note”, etc.)
    -	session_id
	-	source (CLI, project-learning, test, etc.)
	-	timestamp
	-	Text queries (agent ask) and chat sessions store content unless --no-rag is used.
	-	Image queries also store text fragments derived from the description.


## Disabling RAG / History

You can disable memory for a single query:
```bash
agent ask "What is DI?" --no-rag
```

Or start a chat without memory:
```bash
agent chat --no-rag
```

## Writing Notes Manually

You can manually insert notes into memory using Python:
```python
from multimodal_agent import MultiModalAgent

agent = MultiModalAgent()
agent.rag_store.add_logical_message(
    content="This project uses Riverpod.",
    role="note",
    session_id="flutter-app",
    source="manual"
)
```
## Project Learning (v0.6.0+)

The learn-project command scans source code and saves a structured project profile into memory.
```bash
agent learn-project my_flutter_app/
```
Then retrieve:
```bash
agent show-project project:my_flutter_app
```

Project learning integrates seamlessly with history and improves the model’s responses.
