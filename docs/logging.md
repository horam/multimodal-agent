# Logging

The package uses a unified logging utility:

```python
from multimodal_agent.logger import get_logger
logger = get_logger(__name__)
```
---
### Features

- Consistent formatting
- Output to stdout
- Prevents duplicate handlers
- Respects LOGLEVEL environment variable
- Works with pytest caplog
---
### Changing Log Level
In .env:

    LOGLEVEL=DEBUG

Or via CLI:

```bash
agent --debug ask "hello"
```