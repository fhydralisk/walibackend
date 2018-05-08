"""
Exceptions
"""

from django.conf import settings
import traceback


class WLException(Exception):
    message = "Internal error"

    def __init__(self, code, message=None):
        self.code = code
        self.message = message


def Error400(message):
    return WLException(code=400, message=message)


def Error401(message):
    return WLException(code=401, message=message)


def Error403(message):
    return WLException(code=403, message=message)


def Error404(message):
    return WLException(code=404, message=message)


def Error405(message):
    return WLException(code=405, message=message)


def Error409(message):
    return WLException(code=409, message=message)


def Error500(message):
    return WLException(code=500, message=message)


def default_exception(exception):
    def _decorator(func):
        def __decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except WLException:
                raise
            except Exception as e:
                if settings.DEBUG:
                    traceback.print_exc()
                raise exception(str(e))
        return __decorator

    return _decorator
