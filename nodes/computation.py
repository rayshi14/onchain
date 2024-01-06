from abc import ABC, abstractmethod
from .base import *

class AddNode(Node):
    def __init__(self, id: str, deps: dict, params: dict):
        super().__init__(id, deps, params)

    def run(self, ctx: dict, values: dict):
        self.output = values["in1"] + values["in2"]
        self.active = True
        self.finalized = True
        
class CumNode(Node):
    def __init__(self, id: str, deps: dict, params: dict):
        super().__init__(id, deps, params)
        self.output = 0

    def run(self, ctx: dict, values: dict):
        self.output += values["in"]
        self.active = True
        self.finalized = True