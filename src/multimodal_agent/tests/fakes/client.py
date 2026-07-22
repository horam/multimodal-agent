from .models import FakeModels


class FakeClient:
    def __init__(self, text="mocked response"):
        self.models = FakeModels(text)
