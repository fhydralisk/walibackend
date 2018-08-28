"""
User registration functions

Created by Hangyu Fan, May 6, 2018

Last modified: May 6, 2018
"""

import time
from django.contrib.auth import get_user_model
from base.exceptions import *
from base.util.phone_validator import phone_validator
from base.util.misc_validators import validators
from base.util.temp_session import create_session, update_session_dict, \
    destroy_session, get_session_dict, get_session, update_session
from base.util.placeholder2exceptions import get_placeholder2exception
from .session import RegistrationSessionKeys, ValidateStatus

User = get_user_model()


@default_exception(Error500)
def get_sid_by_phonenumber(pn):
    # validate phone number format
    if not validators.validate(pn, "phone number"):
        raise get_placeholder2exception("user/register/pn/pn/ : format of phone number is incorrect")

    # Ensure that user did not access this api recently.
    sid_reverse = RegistrationSessionKeys.PN_2_SID % pn

    try:
        sid_exist = get_session(sid_reverse, RegistrationSessionKeys.SID)
    except KeyError:
        sid_exist = None

    if sid_exist is not None:
        try:
            session_exist = get_session_dict(sid_exist)
        except KeyError:
            session_exist = None
        # If we have a exist session, Then:
        # 1) If the user gives a wrong validation code, this api send the validation code again;
        # 2) If the user does not validate within MIN_INTERVAL, send validation code again;
        # 3) If the user has already successfully validated, but call this api again, re-validate;
        # Otherwise, do nothing.
        if session_exist is not None and not (
            session_exist.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_FAILED or (
                session_exist.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_SENT and
                time.time() - session_exist.get(RegistrationSessionKeys.VCODE_LAST_TIME, 0.0) > ValidateStatus.MIN_INTERVAL
            ) or session_exist.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_SUCCEEDED
        ):
            return sid_exist

        if session_exist is None:
            sid_exist = None

    # send validate message
    vcode = phone_validator.generate_and_send(pn)

    # save validate message into sid
    sid = sid_exist if sid_exist is not None else create_session()

    session = {
        RegistrationSessionKeys.VALIDATE_STATUS: ValidateStatus.VALIDATE_SENT,
        RegistrationSessionKeys.PHONE_NUMBER: pn,
        RegistrationSessionKeys.VCODE: vcode,
        RegistrationSessionKeys.VCODE_LAST_TIME: time.time()
    }
    update_session_dict(sid, session)

    create_session(sid=sid_reverse)
    update_session(sid_reverse, RegistrationSessionKeys.SID, sid)

    # return sid
    return sid


@default_exception(Error500)
def validate_sid(sid, pn, vcode):
    try:
        session = get_session_dict(sid)
    except KeyError:
        raise get_placeholder2exception("user/register/pn/validate/ : sid error")

    if pn != session.get(RegistrationSessionKeys.PHONE_NUMBER):
        raise get_placeholder2exception("user/register/pn/validate/ : sid conflicts with pn")

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_FAILED:
        raise get_placeholder2exception("user/register/pn/validate/ :  Validation error")

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_SUCCEEDED:
        return

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) is None:
        # should not happen but cleanup in case
        destroy_session(sid)
        destroy_session(RegistrationSessionKeys.PN_2_SID % pn)
        raise get_placeholder2exception("user/register/pn/validate/ : sid error")

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_SENT:
        if session.get(RegistrationSessionKeys.VCODE) == vcode:
            session[RegistrationSessionKeys.VALIDATE_STATUS] = ValidateStatus.VALIDATE_SUCCEEDED
            update_session_dict(sid, session)
            return
        else:
            session[RegistrationSessionKeys.VALIDATE_STATUS] = ValidateStatus.VALIDATE_FAILED
            update_session_dict(sid, session)
            raise get_placeholder2exception("user/register/pn/validate/ :  Validation error")

    raise get_placeholder2exception("user/register/pn/validate/ : unexpected fork")


@default_exception(Error500)
def register(sid, pn, password, role):
    try:
        session = get_session_dict(sid)
    except KeyError:
        raise get_placeholder2exception("user/register/pn/password/ : sid error")

    if pn != session.get(RegistrationSessionKeys.PHONE_NUMBER):
        raise get_placeholder2exception("user/register/pn/password/ : sid conflicts with pn")

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_SUCCEEDED:
        if len(User.objects.filter(pn=pn)) != 0:
            raise get_placeholder2exception('user/register/pn/password/ : user exists')

        # Validation is moved to serializers, Below is discarded
        # if not validators.validate(password, "user password"):
        #     raise Error403("Format of password not valid")
        #
        # if not role_choice.validate(role):
        #     raise Error400("role is invalid")

        User.objects.create_user(pn=pn, password=password, role=role)
        # destroy sid
        destroy_session(sid)

    else:
        raise get_placeholder2exception("user/register/pn/password/ : not validated")
