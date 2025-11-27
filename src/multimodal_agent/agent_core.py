import json
import os
import time
from typing import Optional

from google import genai
from google.genai.types import HttpOptions, Part

from multimodal_agent.embedding import embed_text
from multimodal_agent.rag_store import (
    RAGStore,
    SQLiteRAGStore,
    default_db_path,
)

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
        rag_store: RAGStore | None = None,
        enable_rag: bool = True,
        embedding_model: str = "text-embedding-004",
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

        self.rag_store: RAGStore | None = rag_store or SQLiteRAGStore(
            db_path=default_db_path(),
        )
        self.enable_rag = enable_rag
        self.embedding_model = embedding_model

    def safe_generate_content(
        self,
        contents,
        max_retries: int = 3,
        base_delay: int = 1,
        response_format: str = "text",
    ):
        # Detect offline mode (no real API key)
        api_key = os.environ.get("GOOGLE_API_KEY")

        # If client has no real network capability OR no API key → fallback
        if not api_key or not hasattr(self.client, "models"):

            class FakeResponse:
                def __init__(self, contents):
                    for content in contents:
                        self.text = "FAKE_RESPONSE: " + "\n".join(content)

            return FakeResponse(contents)

        if response_format == "json":
            contents = [
                "Return ONLY a valid JSON object without backticks.",
                *contents,
            ]

        for attempt in range(1, max_retries + 1):
            try:
                self.logger.debug(f"Calling Gemini with contents: {contents}")

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                )

                if response_format == "json":
                    return self._convert_to_json_response(response)
                else:
                    return response

            except Exception as exception:
                if is_retryable_error(exception):
                    wait = base_delay * (2 ** (attempt - 1))
                    attempts_message = f"(attempt {attempt}/{max_retries})."
                    self.logger.warning(
                        f"Warning: Model overloaded {attempts_message}.",
                    )
                    self.logger.warning(f"Retry in {wait}s...")
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
    def ask_with_image(
        self,
        question: str,
        image: Part,
        response_format: str = "text",
    ) -> str:
        response = self.safe_generate_content(
            contents=[question, image],
            response_format=response_format,
        )

        if response_format == "json":
            return response.json
        return response.text

    def ask(
        self,
        question: str,
        session_id: Optional[str] = None,
        response_format: str = "text",
    ) -> str:
        """
        One-shot question API.

        If RAG is enabled:
        - store question
        - embed question
        - retrieve similar chunks
        - prepend context to prompt
        - store reply (+ optionally embed reply)
        """
        #  store session id
        session_id = self._ensure_session_id(session_id)

        if self.enable_rag and self.rag_store is not None:
            # store question as a chunk
            question_chunk_ids = self.rag_store.add_logical_message(
                content=question,
                role="user",
                session_id=None,
                source="ask",
            )
            # embed question
            question_embedding = embed_text(
                question,
                model=self.embedding_model,
            )

            # store embedding
            for chunk_id in question_chunk_ids:
                self.rag_store.add_embedding(
                    chunk_id=chunk_id,
                    embedding=question_embedding,
                    model=self.embedding_model,
                )

            # retrieve similar content
            similar = self.rag_store.search_similar(
                query_embedding=question_embedding,
                model=self.embedding_model,
                top_k=5,
            )

            rag_context = [chunk.content for score, chunk in similar]

            system_prompt = (
                "You are a helpful assistant. Use the context if relevant. "
                "otherwise ignore it."
            )

            contents = [
                system_prompt,
                (
                    "RAG CONTEXT:\n" + "\n---\n".join(rag_context)
                    if rag_context
                    else "CONTEXT:\n(none)"
                ),
                "QUESTION:\n" + question,
            ]
        else:
            contents = [question]

        # call model and generate answer
        response = self.safe_generate_content(
            contents,
            response_format=response_format,
        )
        if response_format == "json":
            answer = self._parse_json_output(response.text)
        else:
            answer = response.text

        # store agent reply
        if self.enable_rag and self.rag_store is not None:
            reply_chunk_ids = self.rag_store.add_logical_message(
                content=answer,
                role="agent",
                session_id=session_id,
                source="ask",
            )
            # embed reply too so future questions can reference it
            try:
                reply_emb = embed_text(answer, model=self.embedding_model)
                for chunk_id in reply_chunk_ids:
                    self.rag_store.add_embedding(
                        chunk_id=chunk_id,
                        embedding=reply_emb,
                        model=self.embedding_model,
                    )

            except Exception:
                # Do not crash the CLI if embedding of reply fails
                pass
        return answer

    def _ensure_session_id(self, session_id: Optional[str]) -> str:
        """
        If no session_id is provided, use a stable default or generate one.
        For CLI chat, you might accept a --session flag and pass it through.
        """

        if session_id:
            return session_id

        return "default"

    def _convert_to_json_response(self, response):
        raw = response.text.strip()
        # Remove markdown fences.
        raw = self._strip_markdown(text=raw)

        try:
            objects = json.loads(raw)
            response.json = objects
            return response
        except Exception:
            fallback = {"raw": raw}
            response.json = fallback
            return response
        
    def _parse_json_output(self, text: str):
        stripped = text.strip()

        # Handle fenced code blocks: ```json ... ```
        if stripped.startswith("```"):
            stripped = stripped.strip("`").strip()
        if stripped.startswith("json"):
            stripped = stripped[len("json"):].strip()
        if stripped.endswith("```"):
            stripped = stripped[:-3].strip()

        try:
            return json.loads(stripped)
        except Exception:
            return {"raw": text}
        
    def _strip_markdown(self, text: str) -> str:
        """
        Remove ```json ... ``` fences if the model returns them.
        """
        if text.startswith("```"):
            text = text.strip("`")
            # remove markdown fences like ```json or ```
            text = text.replace("json", "", 1).strip()
        return text


    # Chat mode.
    def chat(
        self,
        session_id: Optional[str] = None,
        enable_rag: Optional[bool] = None,
        rag_top_k: int = 5,
    ) -> str:
        """
        Stateful chat with session-aware memory + RAG.

        Steps:
        - Store user messages (chunked)
        - Embed user messages
        - Retrieve similar chunks
        - Generate response
        - Store + embed assistant responses
        """

        if enable_rag is None:
            enable_rag = self.enable_rag

        # Ensure having a session id.
        session_id = self._ensure_session_id(session_id=session_id)

        self.logger.info(
            "Entering chat mode. Starting chat session"
            f"'{session_id}'. Type 'exit' to quit.",
        )

        while True:
            # remove leading and trailing white spaces.
            user_input = input("You: ").strip()

            if user_input.lower() == "exit":
                self.logger.info("Chat ended. Goodbye!")
                break

            if enable_rag and self.rag_store is not None:
                # store user message as chunk
                user_message_chunk_ids = self.rag_store.add_logical_message(
                    content=user_input,
                    role="user",
                    session_id=session_id,
                    source="chat",
                )

                # embed user message
                try:
                    # return embedding vector
                    question_embedding = embed_text(
                        user_input,
                        model=self.embedding_model,
                    )

                    # add embedding to the store
                    for chunk_id in user_message_chunk_ids:
                        self.rag_store.add_embedding(
                            chunk_id=chunk_id,
                            embedding=question_embedding,
                            model=self.embedding_model,
                        )
                except Exception:
                    question_embedding = None

                # If embedding failed, skip RAG retrieval
                if question_embedding is None:
                    rag_context = []
                else:

                    # Retrieve RAG context from history.
                    similar = self.rag_store.search_similar(
                        query_embedding=question_embedding,
                        model=self.embedding_model,
                        top_k=rag_top_k,
                    )
                    rag_context = [chunk.content for score, chunk in similar]

                # Build final prompt

                system_prompt = (
                    "You are a helpful assistant. Use session history and "
                    "RAG context below if relevant. If not useful, ignore it."
                )
                final_contents = [
                    system_prompt,
                    (
                        "RAG CONTEXT:\n" + "\n---\n".join(rag_context)
                        if rag_context
                        else "RAG CONTEXT:\n(none)"
                    ),
                    "USER MESSAGE:\n" + user_input,
                ]

            else:
                final_contents = [user_input]

            try:
                # call model
                response = self.safe_generate_content(contents=final_contents)
                answer = response.text
            except RetryableError as exception:
                self.logger.error(f"Retryable model failure: {exception}")
                continue

            except AgentError as exception:
                self.logger.error(f"Agent error: {exception}")
                continue

            except NonRetryableError as exception:
                self.logger.error(f"Non-retryable model error: {exception}")
                continue
            print(f"Agent: {answer}")

            if enable_rag and self.rag_store is not None:
                # store assistant reply
                reply_chunk_ids = self.rag_store.add_logical_message(
                    content=answer,
                    role="agent",
                    session_id=session_id,
                    source="chat",
                )

                # embed assistant reply
                try:
                    reply_embedding = embed_text(
                        answer,
                        model=self.embedding_model,
                    )
                    for chunk_id in reply_chunk_ids:
                        self.rag_store.add_embedding(
                            chunk_id=chunk_id,
                            embedding=reply_embedding,
                            model=self.embedding_model,
                        )

                except Exception:
                    pass

                # print answer
                self.logger.info(f"Agent: {answer}")
