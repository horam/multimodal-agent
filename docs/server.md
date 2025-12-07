# Multimodal-Agent Server API

The Multimodal-Agent server exposes a clean HTTP interface to all core agent features:

- Text generation
- Image + text multimodal queries
- JSON mode
- RAG memory search
- Project learning (new in v0.6.0)

Server runs via:

```bash
agent server
```
Default URL:

```bash
http://127.0.0.1:8000
```

### **POST /ask**
---
Send a text prompt to the agent.

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{ "prompt": "hello" }'
```
Response:

```json
{
  "text": "hello",
  "data": null,
  "usage": { "prompt_tokens": 44, "response_tokens": 1, "total_tokens": 553 }
}
```
Supports         |       Field Description |
| -------------- | ----------------------- | 
| response_format  |	"json" or "text"       |
| session_id	 | Custom chat session
| no_rag	   |  Disable RAG for this request

### **POST /ask_with_image**
----
Multipart endpoint for sending an image + prompt.

```bash
curl -X POST http://127.0.0.1:8000/ask_with_image \
  -F "file=@test.jpg" \
  -F "prompt=describe this image"
```
## Error Handling (v0.6.0)
This endpoint now safely handles:

- missing files
- unreadable or corrupted images
- unsupported formats

The server always returns:
---
```json
{ "error": "Invalid or unreadable image file." }
```
instead of crashing.

### **POST /generate**
----
Generate structured JSON or plain text.

```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "give json", "json": true}'
```
Response:

```json
{
  "data": { "x": 42 },
  "text": "{ \"x\": 42 }"
}
```
### **POST /memory/search**
----
Search stored memory (RAG).

```bash
curl -X POST http://127.0.0.1:8000/memory/search \
  -H "Content-Type: application/json" \
  -d '{ "query": "hello", "limit": 5 }'
```
Returns:

```json
{
  "results": [
    [0.91, { "id": 41, "content": "hello", "role": "user" }]
  ]
} 
```
### **POST /memory/summary**
---

If summarization is available, returns a summary of stored memory.
If not available:

```json
{ "summary": "Memory summarization not available." }
```
### **POST /learn/project (v0.6.0)**
---
Learn a Flutter/Dart project structure and store its profile into RAG.

```bash
curl -X POST http://127.0.0.1:8000/learn/project \
  -H "Content-Type: application/json" \
  -d '{ "path": "/abs/path/to/project" }'
```
Response:

```json
{
  "status": "ok",
  "message": "Project learned",
  "project_id": "project:my_app",
  "profile": { ... }
}
```
### **GET /project_profiles/list (v0.6.0)**
List all stored project profiles.

```bash
curl http://127.0.0.1:8000/project_profiles/list
```
Example:

```json
{
  "projects": [
    {
      "project_id": "project:my_app",
      "profile": { "package_name": "my_app" },
      "created_at": "2025-12-07 12:42:58"
    }
  ]
}
```
### **GET /project/{id}**
---
Retrieve a stored profile:

```bash
curl http://127.0.0.1:8000/project/project:my_app
```
### **Server Architecture**
----
Endpoints map directly to internal agent methods (ask, ask_with_image, RAG calls, project scanning).

Fully compatible with future Flutter extension (code generation, project-introspection).