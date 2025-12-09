# **Setting Models**

You can change the default models used by the agent without editing code:
```bash
agent config set-chat-model gemini-1.5-flash
agent config set-image-model gemini-1.5-flash
agent config set-embed-model text-embedding-004
```

Check current configuration:
```
agent config show
```

# CLI Usage

Run the agent directly in terminal:

```bash

agent ask "hello"
```

### **Text Mode**

```bash
agent ask "hello"
```

Disable RAG:

```bash
agent ask "hello"--no-rag
```

JSON mode:

```bash
agent ask "give json"--json
```

## **Image Input**

```bash
agent image test.jpg "describe this"
```

## **Error Handling (v0.6.0)**

When image is missing or corrupted:

```bash
[error] Could not read image file.
```

CLI continues normally.

## **Chat Mode (Persistent)**

```bash

agent chat
```

Stores:

- messages
- chunks
- embeddings

Exit:

```bash
exit
```

## **Server**

Run FastAPI server:

```bash
agent server
```

Includes:

- `/ask`
- `/ask_with_image`
- `/memory/search`
- `/generate`
- `/learn/project (v0.6.0)`

## **Project Learning (v0.6.0)**

Server exposes project-learning endpoints for future Flutter code generation:

- `/learn/project`
- `/project_profiles/list`

CLI itself does not learn projects yet, but the server backend supports it fully.

## **Offline Debug Mode**

If GOOGLE_API_KEY missing:

- text mode works
- image mode returns fake response
- embeddings return deterministic fake vectors
