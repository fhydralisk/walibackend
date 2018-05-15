from .sid_management import sid_getuser


def user_from_sid(exception_no_sid):
    def _decorator(func):
        def __decorator(**kwargs):
            user_sid = kwargs.pop("user_sid", None)
            if user_sid is not None:
                user = sid_getuser(user_sid)
            else:
                user = kwargs.pop("user", None)

            if user is None:
                if exception_no_sid is not None:
                    raise exception_no_sid("No such sid")
                else:
                    return func(user=None, **kwargs)

            return func(user=user, **kwargs)

        return __decorator

    return _decorator
