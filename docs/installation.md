# Installation

Clone the repo:

```bash
git clone https://github.com/horam/multimodal-agent.git
cd multimodal-agent
```
Install in editable mode:

```bash
pip install -e .[dev]
```

Check installation:

```bash
agent --version
```

Create a .env file:


```bash
GOOGLE_API_KEY=your_api_key_here
LOGLEVEL=INFO
```

---


### ✅ `docs/cli.md`

```markdown
# CLI Usage

The package installs a command-line tool called:

agent

shell
Copy code

## Commands

### Ask a text question

```bash
agent ask "What is quantum entanglement?"
Describe an image
bash
Copy code
agent image photo.jpg "what is in this photo?"
Start chat session
bash
Copy code
agent chat
Show version
bash
Copy code
agent --version
Enable debug logs
bash
Copy code
agent --debug ask "hello"
yaml
Copy code

---

### ✅ `docs/agent.md`

```markdown
# The Agent Class

::: multimodal_agent.agent_core.MultiModalAgent
```
