class OfflineModels:
    @staticmethod
    def generate_content(*args, **kwargs):
        raise RuntimeError("Dummy client: no API key available.")


class OfflineClient:
    def __init__(self):
        self.models = OfflineModels()
