from base.exceptions import *
from .utils.usersid import user_from_sid


@default_exception(Error500)
@user_from_sid(Error404)
def get_user_info(user):
    """
    Get user info view obj
    :param user:
    :return: user obj or raise WLException
    """

    return user
