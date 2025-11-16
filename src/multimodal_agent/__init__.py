from .agent_core import MultiModalAgent
from importlib.resources import files

__all__ = ["MultiModalAgent"]

__version__ = (files(__package__) / "VERSION").read_text().strip()
