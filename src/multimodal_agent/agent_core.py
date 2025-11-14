import time
from google import genai
from google.genai.types import HttpOptions, Part
from google.genai.errors import ServerError


class MultiModalAgent:
    def __init__(self, model="gemini-2.5-flash", api_version="v1", client=None):
        if client:
            self.client = client
        else:
            self.client = genai.Client(
                http_options=HttpOptions(api_version=api_version)
            )

        self.model = model

    def safe_generate_content(self, contents, max_retries=3, base_delay=1):
        for attempt in range(1, max_retries + 1):
            try:
                return self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                )

            except ServerError as exception:
                if str(exception.code) == "503":
                    wait = base_delay * (2 ** (attempt - 1))
                    print(
                        f"Warning: Model overloaded (attempt {attempt}/{max_retries}). Retrying in {wait}s..."
                    )
                    time.sleep(wait)
                    continue
                else:
                    raise

            except Exception:
                raise

        print("Model overloaded. Please try again later.")
        return None

    def ask_with_image(self, question: str, image: Part) -> str:
        response = self.safe_generate_content([question, image])
        return response.text

    def ask(self, question: str) -> str:
        response = self.safe_generate_content([question])
        return response.text

    def chat(self):
        print("Welcome to the MultiModal Agent Chat! Type 'exit' to quit.")
        history = []

        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Exiting chat. Goodbye!")
                break

            contents = history + [user_input]
            response = self.safe_generate_content(contents)
            print("Agent:", response.text)
            history.append(user_input)
            response = self.ask(user_input)
            history.append(f"Agent: {response}")
