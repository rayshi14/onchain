from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self, id: str, deps: dict, params: dict):
        self.id = id
        self.deps = deps
        self.params = params
        self.output = None
        self.active = False
        self.finalized = True

    @abstractmethod
    def run(self, ctx: dict, values: dict) -> None:
        pass