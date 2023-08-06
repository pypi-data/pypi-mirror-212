from typing import Any

from . import core
from .abstractions import AgentBase


def factory(name: str) -> AgentBase:
    raise NotImplementedError
