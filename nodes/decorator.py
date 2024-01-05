from abc import ABC, abstractmethod

class Timer(ABC):
    def __init__(self, start, end, frequency):
        self.start = start
        self.end = end
        self.frequency = frequency
        assert self.start <= self.end

    @abstractmethod
    def is_active(self, ctx):
        pass

    @abstractmethod
    def is_expired(self, ctx):
        pass
        
class BlockTimer(Timer):
    def __init__(self, start, end, frequency):
        super().__init__(start, end, frequency)

    def is_active(self, ctx):
        if ctx["block_time"] - self.start >= 0:
            self.start = ((ctx["block_time"] - self.start) // self.frequency + 1) * self.frequency + self.start
            return True
        else:
            return False

    def is_expired(self, ctx):
        if self.start >= self.end:
            return True
        return False

class TimerDecorator:
    def __init__(self, timer_attr):
        self.timer_attr = timer_attr

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            timer = getattr(args[0], self.timer_attr)
            ctx = args[1]
            if not timer.is_expired(ctx) and timer.is_active(ctx):
                func(*args, **kwargs)
        return wrapper