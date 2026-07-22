class FakeImage:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def tobytes(self):
        return b"fakeimage"
