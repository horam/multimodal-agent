# **Multimodal-agent**

*A lightweight, test-covered, production-ready multimodal wrapper for Google Gemini.*

---

## Features

* 🔹 **Text generation**
* 🔹 **Image + text multimodal input**
* 🔹 **Retry logic with exponential backoff**
* 🔹 **Custom exceptions**
* 🔹 **Clean CLI (`agent`)**
* 🔹 **Fully tested (90% coverage)**
* 🔹 **Production logging**
* 🔹 **Simple extensible architecture**

---

## Installation

<pre class="overflow-visible!" data-start="2499" data-end="2539"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install multimodal-agent
</span></span></code></div></div></pre>

(After PyPI release this will work.)

Or install from source:

<pre class="overflow-visible!" data-start="2604" data-end="2632"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install -e .
</span></span></code></div></div></pre>

---

## Usage

### **Text Questions**

<pre class="overflow-visible!" data-start="2676" data-end="2725"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent ask </span><span>"Explain quantum tunneling"</span><span>
</span></span></code></div></div></pre>

### **Image Questions**

<pre class="overflow-visible!" data-start="2752" data-end="2799"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent image cat.jpg </span><span>"Describe this"</span><span>
</span></span></code></div></div></pre>

### **Interactive Chat**

<pre class="overflow-visible!" data-start="2827" data-end="2849"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>agent chat
</span></span></code></div></div></pre>

---

## Python API

<pre class="overflow-visible!" data-start="2874" data-end="2999"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent </span><span>import</span><span> MultiModalAgent

agent = MultiModalAgent()

</span><span>print</span><span>(agent.ask(</span><span>"What is recursion?"</span><span>))
</span></span></code></div></div></pre>

### With images

<pre class="overflow-visible!" data-start="3018" data-end="3270"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent </span><span>import</span><span> MultiModalAgent
</span><span>from</span><span> multimodal_agent.utils </span><span>import</span><span> load_image_as_part

agent = MultiModalAgent()
img = load_image_as_part(</span><span>"car.jpg"</span><span>)

response = agent.ask_with_image(</span><span>"What model is this?"</span><span>, img)
</span><span>print</span><span>(response)
</span></span></code></div></div></pre>

---

## Project Structure

<pre class="overflow-visible!" data-start="3302" data-end="3488"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>multimodal-agent/
│
├── src/multimodal_agent/
│   ├── agent_core.py
│   ├── cli.py
│   ├── utils.py
│   ├── logger.py
│   ├── errors.py
│   └── VERSION
│
├── tests/
└── README.md
</span></span></code></div></div></pre>

---

## Tests

<pre class="overflow-visible!" data-start="3508" data-end="3532"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pytest --cov
</span></span></code></div></div></pre>

Coverage threshold enforced in CI.

---

## Roadmap

* [ ] PyPI release
* [ ] Extra image preprocessing utilities
* [ ] Async version
* [ ] Conversational memory module

---

## License

MIT © 2025 Horam
