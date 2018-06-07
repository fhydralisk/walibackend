"""


"""


class ActionError(Exception):
    pass


class StateError(Exception):
    pass


class SideEffectError(Exception):
    def __init__(self, message=None, exc=None, code=None):
        self.message = message
        self.exc = exc
        self.code = code

    def __str__(self):
        return "SideEffectError, code=%s, exc=%s, message=%s" % (str(self.code), str(self.exc), str(self.message))
