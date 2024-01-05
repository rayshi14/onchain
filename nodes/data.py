from .base import *
from .decorator import *

class DataNode(Node):
    def __init__(self, id: str, deps: dict, params: dict, timer: Timer = None):
        super().__init__(id, deps, params)
        self.timer = timer
    
    @TimerDecorator("timer")
    def run(self, ctx: dict, values: dict) -> None:
        self.output = values
        self.active = True
        self.finalized = True