# **Multimodal-Agent**

*A lightweight, production-ready multimodal wrapper for Google Gemini — with RAG memory, session-based chat, embeddings, retry logic, and a clean CLI.*

---

## Features (v0.2.6)

**Core**

* 🔹 **RAG Memory** (SQLite vector store, embedding retrieval)
* 🔹 **Session-based chat** (`agent chat --session <id>`)
* 🔹 **Cross-session RAG retrieval**
* 🔹 **History management CLI**

  (`show / delete / clear / summary`)
* 🔹 **Text + Image multimodal generation**

**Engine**

* 🔹 **Exponential backoff retry logic**
* 🔹 **Custom exception hierarchy**
* 🔹 **Production logging**
* 🔹 **Extensible & test-covered architecture**

**Tooling**

* 🔹 **Minimal CLI:** `agent`
* 🔹 **94% unit test coverage**

---

## Installation

### From PyPI (recommended)

<pre class="overflow-visible!" data-start="1447" data-end="1487"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install multimodal-agent
</span></span></code></div></div></pre>

### From source

<pre class="overflow-visible!" data-start="1506" data-end="1613"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>git </span><span>clone</span><span> https://github.com/yourname/multimodal-agent.git
</span><span>cd</span><span> multimodal-agent
pip install -e .
</span></span></code></div></div></pre>

---

## Requirements

* Python **3.9+**
* `GOOGLE_API_KEY` set in `.env` file:

<pre class="overflow-visible!" data-start="1698" data-end="1734"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>GOOGLE_API_KEY</span><span>=your_key_here
</span></span></code></div></div></pre>

Dependencies (`google-genai`, `google-adk`) are installed automatically.

---

# CLI Usage

## Ask a question

<pre class="overflow-visible!" data-start="1853" data-end="1902"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent ask </span><span>"Explain quantum tunneling"</span><span>
</span></span></code></div></div></pre>

## Ask about an image

<pre class="overflow-visible!" data-start="1930" data-end="1977"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent image cat.jpg </span><span>"Describe this"</span><span>
</span></span></code></div></div></pre>

## Interactive chat (stateful)

<pre class="overflow-visible!" data-start="2014" data-end="2036"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent chat
</span></span></code></div></div></pre>

## Chat with a custom session

<pre class="overflow-visible!" data-start="2072" data-end="2114"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent chat --session project-x
</span></span></code></div></div></pre>

Each session stores its own memory and embeddings.

---

# RAG Memory (0.2.6+)

Multimodal-Agent now includes a **Retrieval-Augmented Generation (RAG)** engine

powered by an internal SQLite vector store.

### What RAG does:

* Stores all user and assistant messages in a database
* Generates embeddings for each chunk
* Retrieves the most relevant past chunks during answers
* Uses both **current session** and **cross-session** memory
* Improves contextual accuracy

### Disable RAG:

<pre class="overflow-visible!" data-start="2608" data-end="2666"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent chat --no-rag
agent ask </span><span>"hello"</span><span> --no-rag
</span></span></code></div></div></pre>

---

# History Commands (RAG-backed)

### Show recent stored chunks

<pre class="overflow-visible!" data-start="2740" data-end="2781"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent </span><span>history</span><span> show --</span><span>limit</span><span> 20
</span></span></code></div></div></pre>

### Show history for a specific session

<pre class="overflow-visible!" data-start="2824" data-end="2874"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent </span><span>history</span><span> show --session project-x
</span></span></code></div></div></pre>

### Delete a specific chunk

<pre class="overflow-visible!" data-start="2905" data-end="2940"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent </span><span>history</span><span> delete 12
</span></span></code></div></div></pre>

### Clear the entire database

<pre class="overflow-visible!" data-start="2973" data-end="3004"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent </span><span>history</span><span> clear
</span></span></code></div></div></pre>

### Summarize all history using the LLM

<pre class="overflow-visible!" data-start="3047" data-end="3080"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent </span><span>history</span><span> summary
</span></span></code></div></div></pre>

---

# Python API

## Text

<pre class="overflow-visible!" data-start="3113" data-end="3237"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent </span><span>import</span><span> MultiModalAgent

agent = MultiModalAgent()
</span><span>print</span><span>(agent.ask(</span><span>"What is recursion?"</span><span>))
</span></span></code></div></div></pre>

## Image + text

<pre class="overflow-visible!" data-start="3256" data-end="3507"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent </span><span>import</span><span> MultiModalAgent
</span><span>from</span><span> multimodal_agent.utils </span><span>import</span><span> load_image_as_part

agent = MultiModalAgent()
img = load_image_as_part(</span><span>"car.jpg"</span><span>)
response = agent.ask_with_image(</span><span>"What model is this?"</span><span>, img)
</span><span>print</span><span>(response)
</span></span></code></div></div></pre>

---

# Project Structure

<pre class="overflow-visible!" data-start="3538" data-end="4059"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>multimodal-agent/
│
├── src/multimodal_agent/
│   ├── agent_core.py        # Core agent logic (RAG, chat, ask)
│   ├── rag_store.py         # SQLite vector store (chunks + embeddings)
│   ├── embedding.py         # Embedding client </span><span>wrapper</span><span>
│   ├── cli.py               # CLI entrypoint
│   ├── utils.py             # Helpers (images, history)
│   ├── logger.py            # Logging setup
│   ├── errors.py            # Custom exceptions
│   └── </span><span>VERSION</span><span>
│
├── tests/                   # </span><span>90</span><span>%+ coverage
└── README.md
</span></span></code></div></div></pre>

---

# Tests

<pre class="overflow-visible!" data-start="4078" data-end="4098"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>pytest </span><span>--cov</span><span>
</span></span></code></div></div></pre>

Coverage is enforced in CI.

---

# Roadmap

* [X] RAG Memory (0.2.6)
* [ ] Chunk normalization (0.2.7)
* [ ] Token usage logging
* [ ] Async agent (`AsyncMultiModalAgent`)
* [ ] Plugin system (tools, external modules)
* [ ] Flutter extension (planned)
* [ ] IDE extensions (later)
* [ ] Streaming support

---

# 📄 License

MIT © 2025 Horam
