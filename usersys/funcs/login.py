"""
User login/logout functions

Created by Hangyu Fan, May 6, 2018

Last modified: May 6, 2018
"""
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from base.exceptions import *
from usersys.funcs.utils import sid_create, sid_destroy, sid_getuser

User = get_user_model()


@default_exception(Error500)
def login(pn, password):
    # validate username and password
    user = authenticate(pn=pn, password=password)
    if user is None:
        raise Error401("authenticate failed")

    # create SID if match
    sid = sid_create(user)

    # TODO: cache user and sid?

    # return SID
    return sid


@default_exception(Error500)
def logout(sid, pn):
    user = sid_getuser(sid)
    if user is None:
        return

    if user.pn == pn:
        sid_destroy(sid)
    else:
        raise Error409("sid and pn not match")
