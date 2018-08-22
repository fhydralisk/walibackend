from base.exceptions import *
from .utils.usersid import user_from_sid
from base.util.placeholder2exceptions import get_placeholder2exception


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("user/info/self/ : user_sid not exist"))
def get_user_info(user):
    """
    Get user info view obj
    :param user:
    :return: user obj or raise WLException
    """

    return user
