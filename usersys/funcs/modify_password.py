"""
Modify password functions

Created by Hangyu Fan, May 6, 2018

Last modified: May 6, 2018
"""

from django.contrib.auth import get_user_model, authenticate
from base.exceptions import *
from base.util.misc_validators import validators
from base.util.temp_session import destroy_session, get_session_dict
from usersys.models import UserBase

from .session import RegistrationSessionKeys, ValidateStatus
from .utils.usersid import user_from_sid
from usersys.funcs.placeholder2exceptions import get_placeholder2exception

User = get_user_model()


def modify_password(sid, pn, password, role):
    # validate sid to confirm the phone validation process
    session = get_session_dict(sid)
    if session is None:
        raise get_placeholder2exception("user/resetpasswd/pn/validate/ : sid error")
    # validate if sid match pn
    if pn != session.get(RegistrationSessionKeys.PHONE_NUMBER):
        raise get_placeholder2exception("user/resetpasswd/pn/validate/ : pn conflicts with sid")

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_SUCCEEDED:
        # change password and save
        users = User.objects.filter(pn=pn, role=role)
        if len(users) == 0:
            raise get_placeholder2exception("user/resetpasswd/pn/validate/ : sid error")

        if not validators.validate(password, "user password"):
            raise get_placeholder2exception("user/resetpasswd/pn/validate/ : format of password not valid")

        users[0].set_password(password)
        users[0].save()
        # destroy sid
        destroy_session(sid)

    else:
        raise get_placeholder2exception("user/resetpasswd/pn/validate/ : not validated")


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("user/resetpasswd/changepasswd/ : user_sid error"))
def change_password(user, old_password, new_password):
    # type: (UserBase, str, str) -> None
    user = authenticate(pn=user.pn, password=old_password)  # type: UserBase
    if user is None:
        raise get_placeholder2exception("user/resetpasswd/changepasswd/ : Authenticate failed")

    user.set_password(new_password)
    user.save()
