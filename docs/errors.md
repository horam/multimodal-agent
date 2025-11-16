# Errors & Exceptions

The agent defines custom exceptions:

- `AgentError`
- `RetryableError` (503 overload)
- `NonRetryableError`
- `InvalidImageError`

These exceptions are raised by:

- `safe_generate_content`
- `ask_with_image`
- `ask`
- CLI error handling
