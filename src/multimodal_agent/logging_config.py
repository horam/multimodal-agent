import logging


def configure_log(level=logging.info):
    """
    Configure logs. Called from CLI or user code.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
