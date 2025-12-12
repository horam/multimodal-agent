# **Agent Server (FastAPI REST API)**

The Multimodal Agent provides a lightweight HTTP server built on **FastAPI**, allowing external applications (Flutter, web, backend systems) to call the agent over HTTP.

Start the server using:

```
agent server --port 8000
```

The API exposes endpoints for:

* Text generation (**/generate**)
* Image + text multimodal generation (**/generate-image**)
* JSON mode output
* Token usage reporting

---

## **Start the Server**

```
agent server
```

Default port: **8000**

Override:

```
agent server --port 9000
```

---

## **Endpoints Overview**

| **Endpoint** | **Method** | **Description**      |
| ------------------ | ---------------- | -------------------------- |
| /generate          | POST             | Generate from text prompt  |
| /generate-image    | POST             | Generate from text + image |
| /health            | GET              | Health check               |

---

## **Text Generation API**

### **POST /generate**

Request:

```
{
  "prompt": "Write a short poem about stars",
  "response_format": "text",
  "session": "optional-session-id"
}
```

### **Response:**

```
{
  "text": "The stars drift softly...",
  "data": null,
  "usage": {
    "prompt_tokens": 17,
    "response_tokens": 22,
    "total_tokens": 39
  }
}
```

---

## **JSON Mode API**

Request:

```
{
  "prompt": "Return JSON with { name, age }",
  "response_format": "json"
}
```

Response:

```
{
  "text": "{\"name\": \"Alice\", \"age\": 25}",
  "data": {
    "name": "Alice",
    "age": 25
  },
  "usage": {
    "prompt_tokens": 13,
    "response_tokens": 12,
    "total_tokens": 25
  }
}
```

---

## **Image + Text Generation**

### **POST /generate-image**

Supports multimodal input using a base64-encoded image.

Request:

```
{
  "prompt": "Describe this image",
  "image_base64": "<base64 string>",
  "mime_type": "image/jpeg"
}
```

Response:

```
{
  "text": "A cat is sitting on a windowsill...",
  "data": null,
  "usage": {
    "prompt_tokens": 7,
    "response_tokens": 18,
    "total_tokens": 25
  }
}
```

---

## **Offline Mode Behavior**

If **GOOGLE_API_KEY** is missing:

### **Response (text mode)**

```
{
  "text": "FAKE_RESPONSE: <your prompt>",
  "data": null,
  "usage": {
    "prompt_tokens": 10,
    "response_tokens": 5,
    "total_tokens": 15
  }
}
```

Useful for:

* CI testing
* Local development
* Deterministic behavior

---

## **Error Handling**

All errors follow a consistent schema:

```
{
  "error": "Invalid request",
  "detail": "Field 'prompt' is required",
  "status": 400
}
```

Internal agent errors:

```
{
  "error": "ModelError",
  "detail": "Model failed to generate a response",
  "status": 500
}
```

---

## **Example: cURL Commands**

Text:

```
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello"}'
```

Image:

```
curl -X POST http://localhost:8000/generate-image \
  -H "Content-Type: application/json" \
  -d '{"prompt":"What is in this image?", "image_base64":"<...>"}'
```

---

## **Python Client Example**

```
import requests

resp = requests.post(
    "http://localhost:8000/generate",
    json={"prompt": "Hello world"}
)

print(resp.json())
```

---

## **Flutter Client Example**

```
final response = await http.post(
  Uri.parse("http://localhost:8000/generate"),
  headers: {"Content-Type": "application/json"},
  body: jsonEncode({"prompt": "hello"}),
);

final data = jsonDecode(response.body);
print(data["text"]);
```

---

# **Future Server Extensions (v0.9.x)**

The roadmap includes:

* SSE streaming endpoint (**/stream**)
* Code generation endpoint (**/codegen**)
* Endpoint for executing a chain of model calls
* Endpoint for RAG retrieval preview (**/rag/inspect**)
* Built-in authentication tokens

---

## **Summary**

The server:

✔ Provides clean, predictable JSON responses

✔ Supports text, images, and JSON mode

✔ Mirrors the exact behavior of the Python API

✔ Works offline for tests and CI

✔ Integrates cleanly with Flutter, Node, and backend services
