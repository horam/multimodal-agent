### *How sessions work in Multimodal Agent (0.2.6+)*

Sessions allow you to run multiple isolated or parallel conversations using:

* Session-scoped memory
* RAG-based retrieval
* History separation
* Multi-tab CLI workflows (e.g., research1, bugfix2, article-draft)

This document explains how sessions work internally and how to use them in the CLI & Python API.


# What is a Session?

A **session** is simply an ID (string) associated with:

* All messages you send in that session
* All agent responses
* All embeddings generated for those messages

This lets you have:

* Long conversations without mixing contexts
* Multiple independent threads (e.g.,  *project_a* ,  *r1_research* ,  *draft3* )
* Fine-grained RAG memory filtering



# How Sessions Work Internally

### 1. When you pass:

<pre class="overflow-visible!" data-start="987" data-end="1007"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>--session</span><span> s1
</span></span></code></div></div></pre>

The agent automatically:

1. Creates the session if it doesn't exist
2. Stores all chunks in the DB with `session_id = "s1"`
3. Embeds each message (both user + agent)
4. Performs RAG retrieval using:

<pre class="overflow-visible!" data-start="1217" data-end="1330"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>SELECT</span><span> * </span><span>FROM</span><span> embeddings 
</span><span>WHERE</span><span> model = <emb-model> </span><span>AND</span><span> session_id = "s1"
</span><span>ORDER</span><span></span><span>BY</span><span> cosine_similarity </span><span>DESC</span><span>
</span></span></code></div></div></pre>

If `--session` is  **not used** , the messages belong to:

<pre class="overflow-visible!" data-start="1389" data-end="1419"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>session_id</span><span> = </span><span>"default"</span><span>
</span></span></code></div></div></pre>


# RAG + Sessions

With RAG enabled (default):

* RAG searches  **within the same session** , if session is set
* Or **across all sessions** if no session is provided
* Retrieval is filtered by model and chunk role
* The agent constructs a recap-context from top-K chunks
* This recap is inserted *before your prompt*

This improves answer quality in ongoing conversations without polluting unrelated ones.


# Using Sessions in the CLI

### Start a new session:

<pre class="overflow-visible!" data-start="1907" data-end="1953"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent ask </span><span>"hello"</span><span></span><span>--session my_session</span><span>
</span></span></code></div></div></pre>

### Start an isolated chat:

<pre class="overflow-visible!" data-start="1984" data-end="2024"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent chat </span><span>--session</span><span> story_draft
</span></span></code></div></div></pre>

### List session history:

<pre class="overflow-visible!" data-start="2053" data-end="2101"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent history </span><span>show</span><span></span><span>--session story_draft</span><span>
</span></span></code></div></div></pre>

### Summarize session memory:

<pre class="overflow-visible!" data-start="2134" data-end="2185"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent history </span><span>summary</span><span></span><span>--session</span><span> story_draft
</span></span></code></div></div></pre>

### Delete a session (indirectly, via chunks):

<pre class="overflow-visible!" data-start="2235" data-end="2262"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent </span><span>history</span><span></span><span>clear</span><span>
</span></span></code></div></div></pre>



# Using Sessions in Python

### Basic example:

<pre class="overflow-visible!" data-start="2320" data-end="2494"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent </span><span>import</span><span> MultiModalAgent

agent = MultiModalAgent()

resp = agent.ask(
    </span><span>"Summarize this topic"</span><span>,
    session_id=</span><span>"research2"</span><span>,
)
</span><span>print</span><span>(resp)
</span></span></code></div></div></pre>

### With image:

<pre class="overflow-visible!" data-start="2513" data-end="2717"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent.utils </span><span>import</span><span> load_image_as_part

img = load_image_as_part(</span><span>"chart.png"</span><span>)

resp = agent.ask_with_image(
    </span><span>"Explain this chart"</span><span>,
    img,
    session_id=</span><span>"analysis_2025"</span><span>
)
</span></span></code></div></div></pre>

### Chat loop with persisted session:

<pre class="overflow-visible!" data-start="2758" data-end="2806"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>agent.chat(session_id=</span><span>"long_chat"</span><span>)
</span></span></code></div></div></pre>



# Database Structure

Sessions live in the SQLite store:

### `sessions` table

| Column     | Type      | Description                 |
| ---------- | --------- | --------------------------- |
| id         | TEXT PK   | Session ID                  |
| label      | TEXT      | Optional label for UI tools |
| created_at | TIMESTAMP | Auto timestamp              |

### `chunks` table

Each message (user OR agent):

| Column     | Description        |
| ---------- | ------------------ |
| id         | Auto PK            |
| session_id | FK → sessions     |
| role       | user / agent       |
| content    | Text content       |
| source     | chat / ask / image |
| created_at | Auto timestamp     |

### `embeddings` table

Each chunk is embedded once:

| Column    | Description          |
| --------- | -------------------- |
| chunk_id  | FK → chunks         |
| model     | embedding model name |
| dim       | vector dimension     |
| embedding | JSON vector          |



# Testing Sessions

Tests that expect real RAG behavior use:

<pre class="overflow-visible!" data-start="3637" data-end="3676"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>@pytest.mark.use_real_rag</span><span>
</span></span></code></div></div></pre>

Fake store is used automatically for others.



# Recommended Session Strategy

| Use Case                    | Suggested Session            |
| --------------------------- | ---------------------------- |
| Debugging                   | `--session debug`          |
| Research notes              | `--session research_topic` |
| Multi-doc summarization     | `--session docset_2025`    |
| Teaching agent custom rules | `--session persona1`       |
| Story writing               | `--session novel_draft1`   |



# Tips

* Use sessions to  **separate unrelated conversations** .
* RAG becomes significantly more accurate when sessions isolate context.
* You can maintain long-running threads like `career`, `health`, `side_project`.
