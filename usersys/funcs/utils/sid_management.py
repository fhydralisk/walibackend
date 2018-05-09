"""
SID management functions

Created by Hangyu Fan, May 6, 2018

Last modified: May 8, 2018
"""
import uuid
from usersys.models import UserSid
from django.utils.timezone import now


def get_sid(sidstr):
    try:
        sid = UserSid.objects.get(sid=sidstr, is_login=True, expire_datetime__gte=now())
    except UserSid.DoesNotExist:
        return None

    return sid


def sid_to_user(sid):
    # TODO: Cache sid-user map
    sidobj = get_sid(sid)

    return sidobj.uid if sidobj is not None else None


def sid_create(user, ipaddr, duration):
    sid = UserSid.objects.create(
        sid=str(uuid.uuid1()),
        uid=user,
        last_ipaddr=ipaddr,
        is_login=True,
        expire_datetime=now() + duration,
        last_login=now()
    )
    return sid.sid


def sid_access(sid):
    """
    if user access the sid, please call this function
    :param sid:
    """
    # TODO: hook this function into sid model, maybe
    try:
        sidobj = UserSid.objects.get(sid=sid)
        sidobj.last_login = now()
        sidobj.save()
    except UserSid.DoesNotExist:
        pass


def sid_destroy(sid):
    """
    Set sid is_login to False
    :param sid:
    :return:
    """
    sidobj = get_sid(sid)
    if sidobj is not None:
        sidobj.is_login = False
        sidobj.save()
        # TODO: Clean sid-user cache
    else:
        raise KeyError("Sid not exist")


def sid_getuser(sid):
    """
    Get the corresponded user object.
    :param sid:
    :return: corresponded user object
    """
    return sid_to_user(sid)

