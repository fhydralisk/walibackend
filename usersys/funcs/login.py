"""
User login/logout functions

Created by Hangyu Fan, May 6, 2018

Last modified: May 6, 2018
"""
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from base.exceptions import *
from usersys.funcs.utils.sid_management import sid_create, sid_destroy, sid_getuser

from django.conf import settings

User = get_user_model()


@default_exception(Error500)
def login(pn, password, role, ipaddr):
    # validate username and password
    user = authenticate(pn=pn, password=password, role=role)
    if user is None:
        raise Error401("authenticate failed")

    # create SID if match
    sid = sid_create(user, ipaddr, settings.SID_DURATION)

    # TODO: cache user and sid?

    # return SID
    return sid


@default_exception(Error500)
def logout(user_sid, pn):
    user = sid_getuser(user_sid)
    if user is None:
        raise Error404("user_id do not exist")

    if user.pn == pn:
        try:
            sid_destroy(user_sid)
        except KeyError:
            raise Error404("user_id do not exist")
    else:
        raise Error409("user_sid and pn not match")
