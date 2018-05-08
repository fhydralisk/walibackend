"""
Temp session functions

Created by Hangyu Fan, May 6, 2018

Last modified: May 6, 2018
"""
import uuid
from django.core.cache import caches
# TODO: Implement these functions


def check_sid_exist(sid):
    existing = caches["sessions"].get(sid)
    if existing is None:
        raise KeyError("sid not exist")

    return existing


def create_session(sid=None, **kwargs):
    if sid is None:
        sid = "SID_%s" % str(uuid.uuid1())
    caches["sessions"].set(sid, {}, **kwargs)
    return sid


def update_session(sid, key, value, **kwargs):
    existing = check_sid_exist(sid)
    existing[key] = value
    caches["sessions"].set(sid, existing, **kwargs)


def update_session_dict(sid, d, partial=False, **kwargs):
    existing = check_sid_exist(sid)

    if partial:
        caches["sessions"].set(sid, dict(existing, **d), **kwargs)
    else:
        caches["sessions"].set(sid, d, **kwargs)


def get_session(sid, key):
    existing = check_sid_exist(sid)
    return existing[key]


def get_session_dict(sid):
    existing = check_sid_exist(sid)
    return existing


def delete_session_key(sid, key, **kwargs):
    existing = check_sid_exist(sid)
    if key in existing:
        del existing[key]
    
    caches["sessions"].set(sid, existing, **kwargs)


def destroy_session(sid):
    caches["sessions"].delete(sid)
