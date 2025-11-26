# **Multimodal-Agent**

*A lightweight, production-ready multimodal wrapper for Google Gemini — with RAG memory, session-based chat, embeddings, retry logic, and a clean CLI.*

---

## Features (v0.2.7)

**Core**

* 🔹 **RAG Memory** (SQLite vector store, embedding retrieval)
* 🔹 **Session-based chat** (`agent chat --session <id>`)
* 🔹 **Cross-session RAG retrieval**
* 🔹 **History management CLI**

  (`show / delete / clear / summary`)
* 🔹 **Text + Image multimodal generation**

**Engine**

* 🔹 **Token-safe chunking** (sentence-aware, fallback for long text)
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

<pre class="overflow-visible!" data-start="1099" data-end="1135"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>pip</span><span> install multimodal-agent
</span></span></code></div></div></pre>

### From source

<pre class="overflow-visible!" data-start="1154" data-end="1257"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>git </span><span>clone</span><span> https://github.com/yourname/multimodal-agent.git
</span><span>cd</span><span> multimodal-agent
pip install -e .
</span></span></code></div></div></pre>

---

## Requirements

* Python **3.9+**
* `GOOGLE_API_KEY` set in `.env` file:

<pre class="overflow-visible!" data-start="1339" data-end="1375"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>GOOGLE_API_KEY</span><span>=your_key_here
</span></span></code></div></div></pre>

Dependencies (`google-genai`, `google-adk`) are installed automatically.

---

# CLI Usage

## Ask a question

<pre class="overflow-visible!" data-start="1488" data-end="1533"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent</span><span> ask </span><span>"Explain quantum tunneling"</span><span>
</span></span></code></div></div></pre>

## Ask about an image

<pre class="overflow-visible!" data-start="1558" data-end="1601"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent image cat.jpg </span><span>"Describe this"</span><span>
</span></span></code></div></div></pre>

## Interactive chat (stateful)

<pre class="overflow-visible!" data-start="1635" data-end="1653"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent</span><span> chat
</span></span></code></div></div></pre>

## Chat with a custom session

<pre class="overflow-visible!" data-start="1686" data-end="1724"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent chat </span><span>--session</span><span> project-x
</span></span></code></div></div></pre>

Each session stores its own memory and embeddings.

---

# RAG Memory (0.2.6+)

Multimodal-Agent now includes a **Retrieval-Augmented Generation (RAG)** engine powered by an internal SQLite vector store.

### What RAG does:

* Stores all user and assistant messages in a database
* **Splits large messages into normalized chunks before embedding** (0.2.7+)
* Generates embeddings for each chunk
* Retrieves the most relevant past chunks during answers
* Uses both **current session** and **cross-session** memory
* Improves contextual accuracy

### Disable RAG:

<pre class="overflow-visible!" data-start="2289" data-end="2343"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent</span><span> chat --</span><span>no</span><span>-rag
agent ask </span><span>"hello"</span><span> --</span><span>no</span><span>-rag
</span></span></code></div></div></pre>

---

# Chunk Tokenization (0.2.7+)

Multimodal-Agent now includes a robust **token-safe chunking engine** to improve embedding quality and RAG retrieval.

### What this adds:

* Sentence-aware splitting (`split_into_chunks`)
* Paragraph + sentence windowing (`chunk_text`)
* Safe handling of long unbroken strings
* Ensures embeddings stay within expected token limits
* More consistent similarity search results

Tokenization happens **automatically** whenever text is added to the RAG store.

---

# History Commands (RAG-backed)

### Show recent stored chunks

<pre class="overflow-visible!" data-start="2909" data-end="2946"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent </span><span>history</span><span> show --</span><span>limit</span><span> 20
</span></span></code></div></div></pre>

### Show history for a specific session

<pre class="overflow-visible!" data-start="2989" data-end="3035"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent history </span><span>show</span><span></span><span>--session project-x</span><span>
</span></span></code></div></div></pre>

### Delete a specific chunk

<pre class="overflow-visible!" data-start="3066" data-end="3097"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent history </span><span>delete</span><span></span><span>12</span><span>
</span></span></code></div></div></pre>

### Clear the entire database

<pre class="overflow-visible!" data-start="3130" data-end="3157"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent </span><span>history</span><span></span><span>clear</span><span>
</span></span></code></div></div></pre>

### Summarize all history using the LLM

<pre class="overflow-visible!" data-start="3200" data-end="3229"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent </span><span>history</span><span> summary
</span></span></code></div></div></pre>

---

# Python API

## Text

<pre class="overflow-visible!" data-start="3259" data-end="3383"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent </span><span>import</span><span> MultiModalAgent

agent = MultiModalAgent()
</span><span>print</span><span>(agent.ask(</span><span>"What is recursion?"</span><span>))
</span></span></code></div></div></pre>

## Image + text

<pre class="overflow-visible!" data-start="3402" data-end="3653"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent </span><span>import</span><span> MultiModalAgent
</span><span>from</span><span> multimodal_agent.utils </span><span>import</span><span> load_image_as_part

agent = MultiModalAgent()
img = load_image_as_part(</span><span>"car.jpg"</span><span>)
response = agent.ask_with_image(</span><span>"What model is this?"</span><span>, img)
</span><span>print</span><span>(response)
</span></span></code></div></div></pre>

## Chunking Utilities (0.2.7+)

<pre class="overflow-visible!" data-start="3687" data-end="3933"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent.tokenizer </span><span>import</span><span> split_into_chunks
</span><span>from</span><span> multimodal_agent.chunking </span><span>import</span><span> chunk_text

</span><span>print</span><span>(split_into_chunks(</span><span>"very long text..."</span><span>, max_tokens=</span><span>200</span><span>))
</span><span>print</span><span>(chunk_text(</span><span>"paragraphs and sentences..."</span><span>, max_chars=</span><span>800</span><span>))
</span></span></code></div></div></pre>

---

# Project Structure

<pre class="overflow-visible!" data-start="3961" data-end="4617"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>multimodal-agent/
│
├── src/multimodal_agent/
│   ├── agent_core.py        </span><span># Core agent logic (RAG, chat, ask)</span><span>
│   ├── rag_store.py         </span><span># SQLite vector store (chunks + embeddings)</span><span>
│   ├── embedding.py         </span><span># Embedding client wrapper</span><span>
│   ├── tokenizer.py         </span><span># Token-safe chunk splitting (v0.2.7)</span><span>
│   ├── chunking.py          </span><span># Paragraph/sentence chunking (v0.2.7)</span><span>
│   ├── cli.py               </span><span># CLI entrypoint</span><span>
│   ├── utils.py             </span><span># Helpers (images, history)</span><span>
│   ├── logger.py            </span><span># Logging setup</span><span>
│   ├── errors.py            </span><span># Custom exceptions</span><span>
│   └── VERSION
│
├── tests/                   </span><span># 90%+ coverage</span><span>
└── README.md
</span></span></code></div></div></pre>

---

# Tests

<pre class="overflow-visible!" data-start="4633" data-end="4653"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>pytest </span><span>--cov</span><span>
</span></span></code></div></div></pre>

Coverage is enforced in CI.

---

# Roadmap

* [X] RAG Memory (0.2.6)
* [X] **Token-safe chunking (0.2.7)**
* [ ] Token usage logging
* [ ] Async agent (`AsyncMultiModalAgent`)
* [ ] Plugin system (tools, external modules)
* [ ] Flutter extension (planned)
* [ ] IDE extensions (later)
* [ ] Streaming support
