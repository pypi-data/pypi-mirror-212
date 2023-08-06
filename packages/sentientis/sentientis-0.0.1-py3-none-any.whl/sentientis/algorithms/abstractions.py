from typing import Protocol, Any
from abc import abstractmethod


class AlgoBase(Protocol):
    @abstractmethod
    def train(self, *args: Any, **kwargs: Any) -> Any:
        ...
