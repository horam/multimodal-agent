
# Error Handling

The agent defines structured custom exceptions:


## `AgentError`

Base class for all custom agent exceptions.



## `RetryableError`

Raised when:

- Gemini returns HTTP **503**
- Model is overloaded  
- Retries are exhausted  
- Exponential backoff completes without success


## `NonRetryableError`

Raised when:

- The model throws a non-retryable exception  
- Unexpected errors occur in the API call  


## `InvalidImageError`

Raised by:

- `load_image_as_part()`  
- Bad paths  
- Unsupported formats  
- PIL decoding failures  

```python
from multimodal_agent.utils import load_image_as_part
from multimodal_agent.errors import InvalidImageError

try:
    img = load_image_as_part("bad.png")
except InvalidImageError as e:
    print("Could not load image:", e)
```
