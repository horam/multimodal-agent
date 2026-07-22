from importlib.metadata import PackageNotFoundError, version


def get_package_version() -> str:
    try:
        return version("multimodal-agent")
    except PackageNotFoundError:
        return "development"
