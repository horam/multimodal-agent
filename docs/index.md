# Multimodal Agent

A clean, modern multimodal AI agent powered by **Google Gemini**, built by **Horam**.

This library provides:

- Text generation  
- Image + text multimodal prompts  
- Interactive chat mode 
- Local conversation memory 
- Retry logic with exponential backoff  
- Custom exceptions for safe error handling  
- Structured CLI (`agent`)  
- Full logging utilities  
- 85%+ test coverage  
- PyPI-ready project structure  

---


## What’s New (v0.2.0)

- **Local memory system**  
- `agent history show | delete | reset | summary`
- Improved chat mode error handling  
- More modular CLI  
- Updated tests & fixtures  
- Cleaner logging for CLI mode  

---

## Why this project exists

The official Gemini examples are minimal. This package demonstrates how to build a **production-quality, testable, extensible** AI agent with:

- Proper package architecture  
- Retry + failure handling  
- Custom exceptions  
- CLI tooling  
- Strong test coverage  
- Professional project layout  

---

## Documentation

- [Installation](installation.md)  
- [Quickstart](quickstart.md)  
- [CLI Usage](cli.md)  
- [Agent API](agent.md)  
- [Error Handling](errors.md)  
- [Logging](logging.md)  
- [Examples](examples.md)  

---

## Project Structure

```text
multimodal_agent/
├── agent_core.py
├── cli.py
├── utils.py
├── logger.py
├── errors.py
└── tests/
```

---
## Features at a Glance


✔ Gemini API wrapper

✔ Multimodal (text + image)

✔ Retry with exponential backoff

✔ Model overload protection

✔ Custom image loader with MIME detection

✔ CLI tool (agent)

✔ Custom structured logs

✔ Fully tested (85%+)

✔ PyPI-ready packaging