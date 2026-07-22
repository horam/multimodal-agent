from .response import FakeResponse


class FakeModels:
    def __init__(self, text="mocked response"):
        self.text = text

    def generate_content(
        self,
        model,
        contents,
    ):
        return FakeResponse(self.text)
