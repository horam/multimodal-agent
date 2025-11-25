### *Command Line Interface for Multimodal Agent*

The `agent` CLI provides a clean, lightweight way to interact with Google Gemini using:

* Text input
* Image + text multimodal input
* Session-based chat
* RAG-powered history retrieval
* Memory management commands
* Optional verbose metadata output

This page documents all CLI commands for version  **0.2.6+** .



# Installation

Once installed:

<pre class="overflow-visible!" data-start="621" data-end="657"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>pip</span><span> install multimodal-agent
</span></span></code></div></div></pre>

Run:

<pre class="overflow-visible!" data-start="665" data-end="685"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent --</span><span>help</span><span>
</span></span></code></div></div></pre>



# Basic Commands

## **Ask a text question**

<pre class="overflow-visible!" data-start="744" data-end="789"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent</span><span> ask </span><span>"Explain quantum tunneling"</span><span>
</span></span></code></div></div></pre>

### Options:

| Flag                   | Description                                       |
| ---------------------- | ------------------------------------------------- |
| `--session id`       | Use (or create) a session ID, with RAG memory     |
| `--no-rag`           | Disable retrieval                                 |
| `--model model_name` | Override Gemini model                             |
| `--verbose`          | Include metadata fields (tokens, timings, chunks) |

### Example:

<pre class="overflow-visible!" data-start="1085" data-end="1155"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent ask "What are embeddings?" </span><span>--session</span><span> research1 </span><span>--verbose</span><span>
</span></span></code></div></div></pre>



## **Ask with an image**

<pre class="overflow-visible!" data-start="1191" data-end="1240"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent image cat.jpg </span><span>"Describe this image"</span><span>
</span></span></code></div></div></pre>

### Example:

<pre class="overflow-visible!" data-start="1256" data-end="1329"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent image report.png </span><span>"Summarize this chart"</span><span> --session analytics
</span></span></code></div></div></pre>



## **Interactive Chat**

<pre class="overflow-visible!" data-start="1364" data-end="1382"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent</span><span> chat
</span></span></code></div></div></pre>

Start a session-bound chat:

<pre class="overflow-visible!" data-start="1413" data-end="1449"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent chat </span><span>--session</span><span> my_chat
</span></span></code></div></div></pre>

While chatting:

* Your prompts are stored as “chunks”
* Embeddings are added automatically
* RAG retrieves relevant past messages

Exit with:

<pre class="overflow-visible!" data-start="1595" data-end="1612"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>exit</span><span>
quit
</span></span></code></div></div></pre>


# History Commands

## **Show most recent messages**

<pre class="overflow-visible!" data-start="1679" data-end="1705"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent </span><span>history</span><span> show
</span></span></code></div></div></pre>

Optional:

<pre class="overflow-visible!" data-start="1718" data-end="1768"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent </span><span>history</span><span> show --session s1 --</span><span>limit</span><span> 20
</span></span></code></div></div></pre>



## **Delete a specific entry**

<pre class="overflow-visible!" data-start="1810" data-end="1840"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent history </span><span>delete</span><span></span><span>3</span><span>
</span></span></code></div></div></pre>

Deletes by  **chunk ID** .



## **Reset all history**

⚠️ Deletes sessions + chunks + embeddings:

<pre class="overflow-visible!" data-start="1946" data-end="1973"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent </span><span>history</span><span></span><span>clear</span><span>
</span></span></code></div></div></pre>



## **Summarize history using LLM**

<pre class="overflow-visible!" data-start="2019" data-end="2048"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent </span><span>history</span><span> summary
</span></span></code></div></div></pre>

with session filter:

<pre class="overflow-visible!" data-start="2072" data-end="2114"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent history </span><span>summary</span><span></span><span>--session</span><span> s1
</span></span></code></div></div></pre>

This uses the internal agent:

* Loads N recent chunks
* Converts them to summary prompt
* Outputs AI-generated summary


# Verbose Mode (`--verbose`)

Every content generation command supports:

<pre class="overflow-visible!" data-start="2319" data-end="2336"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>--verbose</span><span>
</span></span></code></div></div></pre>

This prints:

<pre class="overflow-visible!" data-start="2352" data-end="2568"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-jsonc"><span>{
  "answer": "...",
  "metadata": {
    "tokens": {...},
    "rag_used": true,
    "session_id": "s1",
    "retrieved_chunks": [
      {"id": 3, "score": 0.81, "preview": "previous message"}
    ]
  }
}
</span></code></div></div></pre>

Verbose mode is designed to be  **machine-readable** , powering:

* Flutter extensions
* VS Code extensions
* CLI debugging tools
* Model introspection tools


# Global Flags

These flags work with every command:

| Flag          | Description                                  |
| ------------- | -------------------------------------------- |
| `--model`   | Set Gemini model (default: gemini-2.5-flash) |
| `--session` | Use/create a named session                   |
| `--no-rag`  | Disable RAG pipeline                         |
| `--verbose` | Output metadata schema                       |
| `--debug`   | Enable debug logging                         |
| `--version` | Show version                                 |



# Testing the CLI

To run CLI tests:

<pre class="overflow-visible!" data-start="3143" data-end="3178"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>pytest tests/test_cli.py -q
</span></span></code></div></div></pre>

To run tests + coverage:

<pre class="overflow-visible!" data-start="3206" data-end="3226"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>pytest </span><span>--cov</span><span>
</span></span></code></div></div></pre>



# Future CLI Enhancements

* Token usage logging
* Chunk-size normalization
* Local tool-calling plugins
* Async CLI via AsyncMultiModalAgent
* Project scaffolding for Flutter + Gemini
