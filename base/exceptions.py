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

    def __call__(self, *args, **kwargs):
        return self


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
