from types import SimpleNamespace

from multimodal_agent.tests.fakes.rag import FakeRAG
from multimodal_agent.tests.fakes.response import FakeResponse


class FakeAgent:

    def __init__(
        self,
        embedding_model="embedding",
        enable_rag=True,
        response=None,
        rag_store=None,
    ):
        self.embedding_model = embedding_model

        # RAG.
        self.enable_rag = enable_rag
        self.rag_store = rag_store or FakeRAG()

        self.response = response
        self.summary = "fake summary"

        self.last_prompt = None
        self.last_image = None
        self.last_kwargs = None

    def ask(
        self,
        prompt,
        data=None,
        prompt_tokens: int = 1,
        response_tokens: int = 1,
        total_tokens: int = 2,
        **kwargs,
    ):

        self.last_prompt = prompt
        self.last_kwargs = kwargs

        if self.response:
            return self.response

        return FakeResponse(
            text=f"echo: {prompt}",
            data=data,
            usage={
                "prompt_tokens": prompt_tokens,
                "response_tokens": response_tokens,
                "total_tokens": total_tokens,
            },
        )

    def ask_with_image(
        self,
        prompt,
        image,
        prompt_tokens: int = 1,
        response_tokens: int = 1,
        total_tokens: int = 2,
    ):

        self.last_prompt = prompt
        self.last_image = image

        if self.response:
            return self.response

        return FakeResponse(
            text=f"echo: {prompt}",
            image=image,
            usage={
                "prompt_tokens": prompt_tokens,
                "response_tokens": response_tokens,
                "total_tokens": total_tokens,
            },
        )

    def summarize_history(self, limit=50, session_id=None):
        return self.summary

    def safe_generate_content(
        self,
        text,
        prompt_tokens: int = 1,
        response_tokens=1,
        total_tokens=2,
        image=None,
        max_retries=3,
        base_delay=1,
        response_format="text",
    ):
        return (
            FakeResponse(text=text, image=image),
            {
                "prompt_tokens": prompt_tokens,
                "response_tokens": response_tokens,
                "total_tokens": total_tokens,
            },
        )

    def boom():
        raise RuntimeError("crash")
