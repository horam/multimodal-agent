# **Multimodal-agent**

*A lightweight, test-covered, production-ready multimodal wrapper for Google Gemini — with clean architecture, CLI, retry logic, and image support.*

---

## Features

* 🔹 **Text generation (simple and robust)**
* 🔹 **Multi modal input (image + text)**
* 🔹 **Exponential backoff retry logic**
* 🔹 **Custom exception hierarchy**
* 🔹 **Minimal, clean CLI command: `agent`**
* 🔹 **90%+ unit test coverage**
* 🔹 **Production-grade logging**
* 🔹 **Extensible architecture (plugins, RAG, memory planned)**

---


## Installation

### **From PyPI (after release)**

<pre class="overflow-visible!" data-start="1029" data-end="1069"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install multimodal-agent
</span></span></code></div></div></pre>

### **From source**

<pre class="overflow-visible!" data-start="1092" data-end="1199"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>git </span><span>clone</span><span> https://github.com/yourname/multimodal_agent.git
</span><span>cd</span><span> multimodal_agent
pip install -e .
</span></span></code></div></div></pre>

---

## Requirements

* **Python 3.9+**
* A valid **Google API key**
* `google-genai` and `google-adk` (installed automatically)

Create a `.env` file in the project root:

<pre class="overflow-visible!" data-start="1377" data-end="1413"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>GOOGLE_API_KEY</span><span>=your_key_here
</span></span></code></div></div></pre>

---

## CLI Usage

### **Ask a text question**

<pre class="overflow-visible!" data-start="1466" data-end="1515"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent ask </span><span>"Explain quantum tunneling"</span><span>
</span></span></code></div></div></pre>

### **Ask about an image**

<pre class="overflow-visible!" data-start="1545" data-end="1592"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent image cat.jpg </span><span>"Describe this"</span><span>
</span></span></code></div></div></pre>

### **Interactive chat session**

<pre class="overflow-visible!" data-start="1628" data-end="1650"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent chat
</span></span></code></div></div></pre>

---

## Python API

### **Basic usage**

<pre class="overflow-visible!" data-start="1696" data-end="1820"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent </span><span>import</span><span> MultiModalAgent

agent = MultiModalAgent()
</span><span>print</span><span>(agent.ask(</span><span>"What is recursion?"</span><span>))
</span></span></code></div></div></pre>

---

### **With images**

<pre class="overflow-visible!" data-start="1848" data-end="2100"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent </span><span>import</span><span> MultiModalAgent
</span><span>from</span><span> multimodal_agent.utils </span><span>import</span><span> load_image_as_part

agent = MultiModalAgent()
img = load_image_as_part(</span><span>"car.jpg"</span><span>)

response = agent.ask_with_image(</span><span>"What model is this?"</span><span>, img)
</span><span>print</span><span>(response)
</span></span></code></div></div></pre>

---

## 📁 Project Structure

<pre class="overflow-visible!" data-start="2132" data-end="2591"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>multimodal-agent/
│
├── src/multimodal_agent/
│   ├── agent_core.py        # Main </span><span>wrapper</span><span> logic
│   ├── cli.py               # CLI entrypoint
│   ├── utils.py             # Helper utilities (image, env loading)
│   ├── logger.py            # Production-ready logging config
│   ├── errors.py            # Custom </span><span>exception</span><span> classes
│   └── </span><span>VERSION</span><span>              # </span><span>Version</span><span> number synced </span><span>to</span><span> PyPI
│
├── tests/                   # ></span><span>90</span><span>% coverage
└── README.md
</span></span></code></div></div></pre>

---

## Tests

<pre class="overflow-visible!" data-start="2611" data-end="2635"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pytest --cov
</span></span></code></div></div></pre>

Coverage enforcement is enabled in CI.

---

## Future Roadmap

* [ ] PyPI release
* [ ] Image preprocessing utilities
* [ ] Async client (`AsyncMultiModalAgent`)
* [ ] Conversational memory module
* [ ] RAG integration / embeddings pipeline
* [ ] Plugin system for tools & external modules
* [ ] Flutter extension (planned)

---

## License

MIT © 2025 Horam
