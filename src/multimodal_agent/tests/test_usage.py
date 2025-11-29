from multimodal_agent import MultiModalAgent


class DummyUsageClient:
    class usage_metadata:
        prompt_token_count = 10
        candidates_token_count = 5
        total_token_count = 15

    class models:
        @staticmethod
        def generate_content(*args, **kwargs):
            class Resp:
                text = "hello"
                usage_metadata = DummyUsageClient.usage_metadata

            return Resp()


def test_usage_in_text_mode():
    agent = MultiModalAgent(enable_rag=False)
    agent.client = DummyUsageClient()

    resp = agent.ask("hello")
    assert resp.text == "hello"
    assert resp.usage["total_tokens"] == 15


def test_usage_in_json_mode():
    class DummyJSON:
        class usage_metadata:
            prompt_token_count = 3
            candidates_token_count = 2
            total_token_count = 5

        class models:
            @staticmethod
            def generate_content(*args, **kwargs):
                class Resp:
                    text = '{"a":1}'
                    usage_metadata = DummyJSON.usage_metadata

                return Resp()

    agent = MultiModalAgent(enable_rag=False)
    agent.client = DummyJSON()

    resp = agent.ask("hi", response_format="json")
    assert resp.data == {"a": 1}
    assert resp.usage["prompt_tokens"] == 3


def test_usage_offline_fake_mode(monkeypatch):
    agent = MultiModalAgent(enable_rag=False)
    monkeypatch.setenv("GOOGLE_API_KEY", "")

    resp = agent.ask("test")
    assert "FAKE_RESPONSE" in resp.text
    assert resp.usage["total_tokens"] > 0
