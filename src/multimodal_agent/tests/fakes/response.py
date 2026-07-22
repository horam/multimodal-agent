class FakeResponse:
    def __init__(
        self,
        text="Mocked response",
        data=None,
        usage=None,
        image=None,
    ):
        self.text = text
        self.data = data
        self.image = None
        self.usage = usage or {
            "prompt_tokens": 1,
            "response_tokens": 1,
            "total_tokens": 2,
        }
