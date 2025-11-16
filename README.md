This installs the `agent` CLI automatically.

---

## 📝 Usage

### **Simple Text Generation**

<pre class="overflow-visible!" data-start="1200" data-end="1367"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent.agent_core </span><span>import</span><span> MultiModalAgent

agent = MultiModalAgent()
response = agent.ask(</span><span>"Tell me something interesting."</span><span>)
</span><span>print</span><span>(response)
</span></span></code></div></div></pre>

---

### **Multimodal: Image + Text**

<pre class="overflow-visible!" data-start="1408" data-end="1683"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent.agent_core </span><span>import</span><span> MultiModalAgent
</span><span>from</span><span> multimodal_agent.utils </span><span>import</span><span> load_image_as_part

agent = MultiModalAgent()

image = load_image_as_part(</span><span>"samples/cat.jpg"</span><span>)
response = agent.ask_with_image(</span><span>"Describe this cat."</span><span>, image)

</span><span>print</span><span>(response)
</span></span></code></div></div></pre>

---

### **Interactive Chat Mode**

<pre class="overflow-visible!" data-start="1721" data-end="1743"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent chat
</span></span></code></div></div></pre>

Example:

<pre class="overflow-visible!" data-start="1755" data-end="1872"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>Welcome </span><span>to</span><span> the MultiModal Agent Chat! Type </span><span>'exit' to quit.</span><span>
</span><span>You:</span><span> hello
</span><span>Agent:</span><span> Hello! How can I help you today?
</span></span></code></div></div></pre>

---

## 🧰 CLI Usage

### **Ask a text question**

<pre class="overflow-visible!" data-start="1925" data-end="1978"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent ask </span><span>"What is quantum entanglement?"</span><span>
</span></span></code></div></div></pre>

### **Describe an image**

<pre class="overflow-visible!" data-start="2007" data-end="2065"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent image photo.jpg </span><span>"what is in this photo?"</span><span>
</span></span></code></div></div></pre>

### **Start chat**

<pre class="overflow-visible!" data-start="2087" data-end="2109"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent chat
</span></span></code></div></div></pre>

---

## 🔍 Logging

The agent uses Python’s `logging` module.

To enable debug logs:

<pre class="overflow-visible!" data-start="2197" data-end="2241"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>LOGLEVEL=DEBUG agent ask </span><span>"hello"</span><span>
</span></span></code></div></div></pre>

Or globally:

<pre class="overflow-visible!" data-start="2257" data-end="2290"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>export</span><span> LOGLEVEL=DEBUG
</span></span></code></div></div></pre>

Debug logs show retries, errors, and internal states.

---

## 🧪 Testing

Tests use:

* `pytest`
* `pytest-mock`
* Fully mocked Gemini API (no network, no cost)

Run tests:

<pre class="overflow-visible!" data-start="2467" data-end="2488"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pytest -q
</span></span></code></div></div></pre>

Run with coverage:

<pre class="overflow-visible!" data-start="2510" data-end="2577"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pytest --cov=multimodal_agent --cov-report=term-missing
</span></span></code></div></div></pre>

---

## 🏛 Project Structure

<pre class="overflow-visible!" data-start="2609" data-end="2994"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>multimodal-agent/
├── pyproject</span><span>.toml</span><span>
├── README</span><span>.md</span><span>
├── Makefile
├── </span><span>src</span><span>/
│   └── multimodal_agent/
│       ├── agent_core</span><span>.py</span><span>
│       ├── cli</span><span>.py</span><span>
│       ├── utils</span><span>.py</span><span>
│       ├── logger</span><span>.py</span><span>
│       ├── VERSION
│       └── tests/
│           ├── test_agent_core</span><span>.py</span><span>
│           ├── test_cli</span><span>.py</span><span>
│           └── conftest</span><span>.py</span><span>
└── examples/
    ├── simple_text</span><span>.py</span><span>
    └── simple_image</span><span>.py</span><span>
</span></span></code></div></div></pre>

---

## 🧩 Architecture Overview

### **AgentCore**

Handles:

* model initialization
* retry logic
* multimodal calls
* chat history
* safe request execution

### **Utils**

* load images from file or URL
* environment helpers

### **CLI**

Implements:

* `agent ask`
* `agent image`
* `agent chat`

### **Logger**

* production-grade logging
* configurable via `LOGLEVEL`

### **Tests**

* fully isolated
* mocked API
* deterministic

---

## 🧭 Roadmap

* [ ] async agent (`MultiModalAgentAsync`)
* [ ] streaming support in CLI
* [ ] audio → text input
* [ ] OCR helpers
* [ ] mkdocs documentation website
* [ ] TestPyPI + PyPI deployment workflow

---

## 🧑‍💻 Development Tools

The project includes a Makefile:

<pre class="overflow-visible!" data-start="3732" data-end="4004"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>make install       </span><span># install dependencies</span><span>
make </span><span>test</span><span></span><span># run tests</span><span>
make coverage      </span><span># run coverage</span><span>
make format        </span><span># black + isort</span><span>
make build         </span><span># build wheel and sdist</span><span>
make publish-test  </span><span># upload to TestPyPI</span><span>
make publish       </span><span># upload to PyPI</span><span>
</span></span></code></div></div></pre>

---

## 👤 Author

**Horam**

---
