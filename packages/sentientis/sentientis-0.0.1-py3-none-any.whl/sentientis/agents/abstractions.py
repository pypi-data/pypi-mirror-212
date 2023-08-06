from typing import Protocol, Any
from abc import abstractmethod


class AgentBase(Protocol):
    @abstractmethod
    def predict(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @abstractmethod
    def train(self, *args: Any, **kwargs: Any) -> Any:
        ...

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.predict(*args, **kwargs)
