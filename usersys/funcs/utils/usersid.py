from .sid_management import sid_getuser


def user_from_sid(exception_no_sid):
    def _decorator(func):
        def __decorator(user_sid, *args, **kwargs):
            user = sid_getuser(user_sid)
            if user is None:
                raise exception_no_sid("No such sid")
            return func(*args, user=user, **kwargs)

        return __decorator

    return _decorator
