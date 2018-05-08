"""
Modify password functions

Created by Hangyu Fan, May 6, 2018

Last modified: May 6, 2018
"""

from django.contrib.auth import get_user_model
from base.exceptions import *
from base.util.misc_validators import validators
from base.util.temp_session import destroy_session, get_session_dict

from .session import RegistrationSessionKeys, ValidateStatus

User = get_user_model()


def modify_password(sid, pn, new_passwd):
    # validate sid to confirm the phone validation process
    session = get_session_dict(sid)
    if session is None:
        raise Error404("Sid does not exist")

    # validate if sid match pn
    if pn != session.get(RegistrationSessionKeys.PHONE_NUMBER):
        raise Error409("Validation code not match")

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_SUCCEEDED:
        # change password and save
        users = User.objects.filter(pn=pn)
        if len(users) == 0:
            raise Error404("User does not exist")

        if not validators.validate(new_passwd, "user password"):
            raise Error403("Format of password not valid")

        users[0].set_password(new_passwd)
        users[0].save()
        # destroy sid
        destroy_session(sid)

    else:
        raise Error405("Not validated")
