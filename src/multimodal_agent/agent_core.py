import os
import time

from google import genai
from google.genai.types import HttpOptions, Part

from .errors import AgentError, NonRetryableError, RetryableError
from .logger import get_logger


def is_retryable_error(exception):
    # Example: Gemini overload has status_code = 503
    return hasattr(exception, "status_code") and exception.status_code == 503


class MultiModalAgent:
    def __init__(
        self,
        model="gemini-2.5-flash",
        api_version="v1",
        client=None,
    ):
        self.logger = get_logger(__name__)
        self.logger.info("Initializing MultiModal agent...")

        self.model = model

        if client is not None:
            self.client = client
        else:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                # In CI or local without key, use dummy client
                class DummyClient:
                    class models:
                        @staticmethod
                        def generate_content(*a, **k):
                            raise RuntimeError(
                                "Real model not available (no API key).",
                            )

                self.client = DummyClient()
            else:
                self.client = genai.Client(
                    http_options=HttpOptions(api_version=api_version),
                )

    # safe request execution with retries.
    def safe_generate_content(self, contents, max_retries=3, base_delay=1):
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.debug(f"Calling Gemini with contents: {contents}")

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                )
                return response

            except Exception as exception:
                if is_retryable_error(exception=exception):
                    wait = base_delay * (2 ** (attempt - 1))
                    message = "(attempt {attempt}/{max_retries})."
                    self.logger.warning(f"Warning: Model overloaded {message}")
                    self.logger.warning(f" Retry in {wait}s...")
                    time.sleep(wait)
                    continue

                self.logger.error(
                    "Non-retryable error occurred.",
                    exc_info=True,
                )
                raise NonRetryableError(str(exception)) from exception

        self.logger.error("Model overloaded. Please try again later.")
        raise RetryableError("Model overloaded after maximum retry attempts.")

    # Public methods.
    def ask_with_image(self, question: str, image: Part) -> str:
        response = self.safe_generate_content([question, image])
        return response.text

    def ask(self, question: str) -> str:
        response = self.safe_generate_content([question])
        return response.text

    # Chat mode.
    def chat(self):
        self.logger.info(
            "Welcome to the MultiModal Agent Chat! Type 'exit' to quit.",
        )
        history = []

        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                self.logger.info("Chat session ended. Goodbye!")
                break
            # Create conversation history.
            contents = history + [user_input]
            try:
                response = self.safe_generate_content(contents)
            except AgentError as exception:
                self.logger.error(f"Agent failed: {exception}")
                continue

            answer = response.text
            self.logger.info(f"Agent: {answer}")

            # update chat history
            history.append(user_input)
            history.append(answer)
