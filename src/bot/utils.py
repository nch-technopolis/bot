

class Triggerable:
    def __init__(self, trigger):
        self.trigger = trigger

    def triggered(self, *args, **kwargs):
        return self.trigger(*args, **kwargs)
