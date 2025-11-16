# Logging

The project uses a custom logger:

```python
from multimodal_agent.logger import get_logger
```
It supports:

* consistent formatting

* LOGLEVEL override via environment

* stdout handler

* works with pytest caplog

