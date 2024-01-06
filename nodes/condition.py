from .base import *

class ThresholdNode(Node):
    def __init__(self, id: str, deps: dict, params: dict):
        super().__init__(id, deps, params)

    def run(self, ctx: dict, values: dict):
        if self.params["condition"] == "gt":
            if values["in"] > self.params["th"]:
                self.active = True
                self.finalize = True
        elif self.params["condition"] == "ge":
            if values["in"] >= self.params["th"]:
                self.active = True
                self.finalize = True
        elif self.params["condition"] == "lt":
            if values["in"] < self.params["th"]:
                self.active = True
                self.finalize = True
        elif self.params["condition"] == "le":
            if values["in"] <= self.params["th"]:
                self.active = True
                self.finalize = True