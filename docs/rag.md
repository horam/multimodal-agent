### *Retrieval-Augmented Generation (RAG) in Multimodal Agent (0.2.6+)*

RAG enhances your agent by giving it  **persistent memory** ,  **context retrieval** , and **long-range recall** across sessions.

This document explains:

* What RAG is
* How it works inside `multimodal_agent`
* The embedding pipeline
* Storage layout (SQLite)
* Retrieval algorithm
* How to enable/disable it
* Testing strategy

---

# What is RAG?

**RAG = Retrieval-Augmented Generation**

Your messages are:

1. **Stored** as chunks
2. **Embedded** into numerical vectors
3. **Retrieved** based on similarity when answering new prompts

This allows the model to recall:

* Prior discussions
* Long-running chats
* Multi-step reasoning
* Project-specific information
* Custom rules or preferences

RAG dramatically improves coherence and personalization.

---

# How RAG Works in Multimodal Agent

The full RAG pipeline:

<pre class="overflow-visible!" data-start="1191" data-end="1378"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>USER</span><span> MESSAGE
    ↓
Store </span><span>as</span><span> chunk → Embed → Save vector
    ↓
Retrieve </span><span>similar</span><span> chunks (KNN </span><span>search</span><span>)
    ↓
Construct augmented prompt
    ↓
Generate </span><span>final</span><span> answer </span><span>using</span><span> Google Gemini
</span></span></code></div></div></pre>

---

# Chunk Structure

Every message (user + agent) becomes a  **chunk** :

<pre class="overflow-visible!" data-start="1461" data-end="1625"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-json"><span><span>{</span><span>
  </span><span>"id"</span><span>:</span><span></span><span>42</span><span>,</span><span>
  </span><span>"session_id"</span><span>:</span><span></span><span>"s1"</span><span>,</span><span>
  </span><span>"role"</span><span>:</span><span></span><span>"user"</span><span>,</span><span>
  </span><span>"content"</span><span>:</span><span></span><span>"Explain reactive power"</span><span>,</span><span>
  </span><span>"source"</span><span>:</span><span></span><span>"chat"</span><span>,</span><span>
  </span><span>"created_at"</span><span>:</span><span></span><span>"2024-02-01T12:22:11"</span><span>
</span><span>}</span><span>
</span></span></code></div></div></pre>

Why chunks?

* Separates text from metadata
* Enables easy indexing & filtering
* Plays nicely with embeddings

---

# Embedding Pipeline

When a chunk is added:

<pre class="overflow-visible!" data-start="1802" data-end="1876"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>content</span><span> → embedding model → </span><span>[vector]</span><span> → store in “embeddings” </span><span>table</span><span>
</span></span></code></div></div></pre>

Embedding definition:

<pre class="overflow-visible!" data-start="1901" data-end="2017"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-json"><span><span>{</span><span>
  </span><span>"chunk_id"</span><span>:</span><span></span><span>42</span><span>,</span><span>
  </span><span>"model"</span><span>:</span><span></span><span>"text-embedding-004"</span><span>,</span><span>
  </span><span>"dim"</span><span>:</span><span></span><span>768</span><span>,</span><span>
  </span><span>"embedding"</span><span>:</span><span></span><span>"[0.12, -0.55, ...]"</span><span>
</span><span>}</span><span>
</span></span></code></div></div></pre>

Your implementation ensures:

* deterministic embedding calls
* re-embedding only if missing
* composable design for custom models later

---

# Storage Backend (SQLite)

Multimodal Agent uses a lightweight, portable SQLite DB:

### `sessions`

Tracks all chat threads.

### `chunks`

Stores every message.

### `embeddings`

Stores numeric vectors for similarity search.

🎯 Reasons for SQLite:

* Zero dependencies
* Easy to bundle with Flutter extensions
* Perfect for local/offline memory
* Very fast for small-to-medium RAG workloads

---

# Retrieval Algorithm (Similarity Search)

When a new question arrives:

### Step 1 — Embed the query text

(same embedding model as chunks)

### Step 2 — Retrieve top-k similar chunks

<pre class="overflow-visible!" data-start="2774" data-end="2843"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-sql"><span><span>SELECT</span><span> chunk_id, embedding </span><span>FROM</span><span> embeddings
</span><span>WHERE</span><span> model </span><span>=</span><span> ?
</span></span></code></div></div></pre>

### Step 3 — Compute cosine similarity

<pre class="overflow-visible!" data-start="2885" data-end="2944"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>score </span><span>=</span><span> dot</span><span>(</span><span>query</span><span>, emb</span><span>)</span><span> / </span><span>(</span><span>norm</span><span>(</span><span>query</span><span>)</span><span> * norm</span><span>(</span><span>emb</span><span>)</span><span>)</span><span>
</span></span></code></div></div></pre>

### Step 4 — Return top results

Your implementation returns:

<pre class="overflow-visible!" data-start="3009" data-end="3047"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>[(similarity_score, Chunk), …]</span><span>
</span></span></code></div></div></pre>

### Step 5 — Build augmented prompt

<pre class="overflow-visible!" data-start="3086" data-end="3151"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>[</span><span>SUMMARY</span><span></span><span>OF</span><span> RELEVANT HISTORY]
</span><span>User</span><span>: <your actual message>
</span></span></code></div></div></pre>

This augmentation is  **transparent and automatic** .

---

# Why RAG Matters for This Project

Your agent becomes:

* More personal
* More helpful over time
* Better at tracking context
* Able to recall long, multi-step conversations
* Capable of advanced workflows (research, writing, debugging)

And in the future:

**RAG will power your Flutter plugin** for:

* Project-wide recall
* Natural-language code generation
* Memory inside dev tools & IDEs

---

# Testing Strategy

RAG code is isolated behind:

<pre class="overflow-visible!" data-start="3689" data-end="3711"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>SQLiteRAGStore</span><span>
</span></span></code></div></div></pre>

Two modes are used in tests:

### **Fake store (default)**

Used for all non-RAG tests

Ensures stability and speed

Prevents accidental DB operations

### **Real store (`@pytest.mark.use_real_rag`)**

Tests database logic & embed/search flow

Your `conftest.py` handles this automatically.

---

# Enabling / Disabling RAG

### RAG enabled by default

<pre class="overflow-visible!" data-start="4076" data-end="4101"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent</span><span> ask </span><span>"hello"</span><span>
</span></span></code></div></div></pre>

### Disable RAG

<pre class="overflow-visible!" data-start="4120" data-end="4154"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent</span><span> ask </span><span>"hello"</span><span> --</span><span>no</span><span>-rag
</span></span></code></div></div></pre>

### Session-specific RAG

<pre class="overflow-visible!" data-start="4182" data-end="4268"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent chat </span><span>--session</span><span> research2025
agent history </span><span>summary</span><span></span><span>--session</span><span> research2025
</span></span></code></div></div></pre>

---

# RAG Limitations

* No chunk-size normalization yet (coming next)
* Embeddings are stored for full messages; splitting not implemented
* No embedding caching between models
* No multi-model index
* No hybrid search (BM25 + embeddings)

These are planned improvements.

---

# Roadmap for RAG

### 0.2.6 — RAG v1

* Chunk storage
* Embedding pipeline
* KNN search
* Session integration
* Summaries and history tools
* Tests for all parts

### 0.2.7 — Chunk Normalization

* Split long messages into manageable chunks
* Normalize to N characters
* Add chunk headers
* Improve recall accuracy

### 0.2.8 — Query Expansion

* Use model to rewrite user queries
* Improve retrieval

### 0.3.x — Embedding Cache

* DB-level dedupe
* Hash-based cache

### 0.4.x — Hybrid Search

* BM25 + embeddings combined

---

# Summary

RAG transforms your agent from a basic API wrapper into a **stateful, context-aware assistant** with:

* Memory
* Recall
* Context stitching
* Session isolation
* Accurate and meaningful retrieval

This document gives developers full insight into how to extend or integrate RAG with future tools (including the upcoming Flutter extension).
