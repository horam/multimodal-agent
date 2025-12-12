# Installation

Multimodal-Agent is a lightweight wrapper around Google Gemini with support for
RAG, multimodal input (text + image), and Flutter code generation.

This guide explains how to install and configure the library.


## Install via pip

```bash
pip install multimodal-agent
```
To upgrade:
```bash
pip install -U multimodal-agent
```

## Install from source
```bash
git clone https://github.com/horam/multimodal-agent.git
cd multimodal-agent
pip install -e .[dev,test]
```

## Set up your API key

Multimodal-Agent automatically loads keys from:

-	environment variable
-   .env file in project root
-   agent config set-key

**Option A — Environment variable**

```bash
export GOOGLE_API_KEY="your-key-here"
```

**Option B — .env file (recommended for local projects)**

Create:
```bash
.env
```

Inside:
```bash
GOOGLE_API_KEY=your-key-here
```

## Offline Fake Mode (no API key)

If no key is provided the agent still works, using predictable fake responses.
```python
from multimodal_agent.core.agent_core import MultiModalAgent

agent = MultiModalAgent()
print(agent.ask("hello").text) # -> FAKE_RESPONSE: hello
```

This is ideal for:
-   testing
-   CI pipelines
-   environments without network access


## Additional Optional Dependencies

Some features require additional tools:

**RAG (SQLite-based)**

No extra installation needed — SQLite is built-in.

**FastAPI Server**

If you want server mode:
```bash
pip install multimodal-agent[server]
```

Documentation generation (for maintainers)
```bash
pip install multimodal-agent[dev]
```


## Flutter Code Generation Requirements (v0.8.0+)

To generate widgets, screens, and models, the CLI must run inside a valid Flutter project root (one containing a pubspec.yaml).

Example:
```bash
cd my_flutter_app
agent gen widget CoolWidget
```

Generated files are placed automatically:
```bash
lib/widgets/
lib/screens/
lib/models/
```

## Verify Installation
```bash
agent --version
```
Expected output:
```bash
multimodal-agent version 0.8.0
```

Test API access:
```bash
agent ask "hello"
```

If key is missing, you will see:
```bash
FAKE_RESPONSE: hello
```

## Troubleshooting

“Could not find pubspec.yaml”

Move into your Flutter project directory:
```bash
cd path/to/app
```

**“No such file or directory: image”**

Ensure the image exists before using:
```bash
agent image ./photo.png "describe"
```

**“Invalid API key”**

Check:
```bash
echo $GOOGLE_API_KEY
```

## Next Steps

Continue with:
-	CLI Usage￼
-	Quickstart Tutorial￼
-	RAG System￼
