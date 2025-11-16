# **Multimodal Agent**

*A clean, modern multimodal AI agent using Google Gemini — built by Horam.*

---

## Features

This package provides a **robust, production-ready multimodal agent** with:

* ✔ **Text generation**
* ✔ **Image + text multimodal prompts** (Part API)
* ✔ **Interactive Chat Mode**
* ✔ **Retry logic** (handles 503 model overload automatically)
* ✔ **Sync & Async** agent versions (coming soon)
* ✔ **CLI tool** (`agent`) for terminal usage
* ✔  **Logging** ,  **testing** ,  **coverage** , **mocking**
* ✔ **Clean architecture** suitable for extension & production deployment

---

## Installation

From source:

<pre class="overflow-visible!" data-start="888" data-end="997"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>git </span><span>clone</span><span> https://github.com/horam/multimodal-agent.git
</span><span>cd</span><span> multimodal-agent
pip install -e .[dev]
</span></span></code></div></div></pre>

After installation, the `agent` CLI becomes available:

<pre class="overflow-visible!" data-start="1055" data-end="1084"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent ask </span><span>"hello"</span><span>
</span></span></code></div></div></pre>

---

## Usage 

### **Simple text generation**

<pre class="overflow-visible!" data-start="1145" data-end="1312"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent.agent_core </span><span>import</span><span> MultiModalAgent

agent = MultiModalAgent()
response = agent.ask(</span><span>"Tell me something interesting."</span><span>)
</span><span>print</span><span>(response)
</span></span></code></div></div></pre>

---

### **Multimodal (image + text)**

<pre class="overflow-visible!" data-start="1354" data-end="1629"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent.agent_core </span><span>import</span><span> MultiModalAgent
</span><span>from</span><span> multimodal_agent.utils </span><span>import</span><span> load_image_as_part

agent = MultiModalAgent()

image = load_image_as_part(</span><span>"samples/cat.jpg"</span><span>)
response = agent.ask_with_image(</span><span>"Describe this cat."</span><span>, image)

</span><span>print</span><span>(response)
</span></span></code></div></div></pre>

---

### **Interactive Chat Mode**

<pre class="overflow-visible!" data-start="1667" data-end="1685"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>agent</span><span> chat
</span></span></code></div></div></pre>

Example:

<pre class="overflow-visible!" data-start="1697" data-end="1814"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>Welcome </span><span>to</span><span> the MultiModal Agent Chat! Type </span><span>'exit' to quit.</span><span>
</span><span>You:</span><span> hello
</span><span>Agent:</span><span> Hello! How can I help you today?
</span></span></code></div></div></pre>

---

## CLI Usage

The package installs a command-line tool called  **`agent`** .

### **Ask a text question**

<pre class="overflow-visible!" data-start="1929" data-end="1982"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent ask </span><span>"What is quantum entanglement?"</span><span>
</span></span></code></div></div></pre>

---

### **Describe an image**

<pre class="overflow-visible!" data-start="2016" data-end="2074"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent image photo.jpg </span><span>"what is in this photo?"</span><span>
</span></span></code></div></div></pre>

---

### **Start a chat session**

<pre class="overflow-visible!" data-start="2111" data-end="2133"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent chat
</span></span></code></div></div></pre>

---

## Configuration & Logging

The agent uses Python’s `logging` module instead of prints.

To enable debug logs:

<pre class="overflow-visible!" data-start="2255" data-end="2292"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent --debug ask </span><span>"hello"</span><span>
</span></span></code></div></div></pre>

Or inside Python:

<pre class="overflow-visible!" data-start="2313" data-end="2419"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent.logging_config </span><span>import</span><span> configure_log
configure_logging(level=</span><span>"DEBUG"</span><span>)
</span></span></code></div></div></pre>

All internal retries and errors will be logged cleanly.

---

## 🧪 Testing

Tests use  **pytest** ,  **pytest-mock** , and **100% mocked Gemini calls** (no API cost).

Run tests:

<pre class="overflow-visible!" data-start="2598" data-end="2619"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pytest -q
</span></span></code></div></div></pre>

Run tests with coverage:

<pre class="overflow-visible!" data-start="2647" data-end="2714"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pytest --cov=multimodal_agent --cov-report=term-missing
</span></span></code></div></div></pre>

---

## 🏛 Project Structure

<pre class="overflow-visible!" data-start="2761" data-end="3141"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>multimodal-agent/
├── pyproject</span><span>.toml</span><span>
├── README</span><span>.md</span><span>
├── </span><span>src</span><span>/
│   └── multimodal_agent/
│       ├── agent_core</span><span>.py</span><span>
│       ├── cli</span><span>.py</span><span>
│       ├── utils</span><span>.py</span><span>
│       ├── logging_config</span><span>.py</span><span>
│       └── tests/
│           ├── test_agent_core</span><span>.py</span><span>
│           ├── test_cli</span><span>.py</span><span>
│           └── conftest</span><span>.py</span><span>
└── examples/
    ├── simple_text</span><span>.py</span><span>
    └── simple_image</span><span>.py</span><span>
</span></span></code></div></div></pre>

This layout follows modern Python packaging best practices.

---

## 🧩 Architecture Overview

### **AgentCore**

Handles:

* model initialization
* retry logic
* multimodal requests
* chat history
* safe request execution

### **Utils**

Handles:

* loading images from file or URL
* environment handling

### **CLI**

Provides:

* `ask`
* `image`
* `chat`

### **Tests**

Fully mocked, fast, network-isolated.

---

## 🧭 Roadmap

* [ ] Add async agent (`MultiModalAgentAsync`)
* [ ] Add streaming responses in CLI
* [ ] Add audio input support
* [ ] Add vision+OCR utilities
* [ ] Publish to PyPI (`multimodal-agent`)
* [ ] Add mkdocs documentation site
* [ ] Add PyPI deployment GitHub Action

---

## 🧑‍💻 Development

This project includes a `Makefile` to simplify common tasks:

<pre class="overflow-visible!" data-start="1069" data-end="1389"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>make install      </span><span># install package in editable mode + dev dependencies</span><span>
make </span><span>test</span><span></span><span># run tests</span><span>
make coverage     </span><span># run tests with coverage report</span><span>
make format       </span><span># apply black + isort</span><span>
make build        </span><span># build wheel and sdist</span><span>
make publish-test </span><span># upload to TestPyPI</span><span>
make publish      </span><span># upload to PyPI</span><span>
</span></span></code></div></div></pre>


---

## 👤 Author

Built with by **Horam**
