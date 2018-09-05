from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error500, Error404, WLException, default_exception
from demandsys.util.unit_converter import UnitQuantityMetric
from usersys.models import UserBase
from usersys.model_choices.user_enum import role_choice
from simplified_invite.models import InviteInfo
from simplified_invite.model_choices.invite_enum import i_status_choice


@default_exception(Error500)
@user_from_sid(Error404)
def submit_invite(user, invite):
    # type: (UserBase, dict, list) -> QuerySet
    if not user.is_validated():
        raise WLException(410, "user's validataion does not passed, can't submit")

    # Validate whether
    invite["dmid_t"].validate_satisfy_demand(
        user.role, quantity=invite["quantity"]
    )

    invite_obj = InviteInfo(uid_s=user, **invite)

    # invite_obj.uid_s = user,
    invite_obj.uid_t = invite["dmid_t"].uid
    invite_obj.i_status = i_status_choice.STARTED

    invite_obj.save()

    return invite_obj


@default_exception(Error500)
@user_from_sid(Error404)
def cancel_invite(user, ivid, reason_id, reason):
    # type: (UserBase, int) -> QuerySet
    if not user.is_validated():
        raise WLException(410, "user's validataion does not passed")

    try:
        invite_obj = InviteInfo.objects.get(id=ivid)
    except InviteInfo.DoesNotExist:
        raise WLException(404, "no such ivid")

    if not user == invite_obj.uid_s or not user.role == role_choice.BUYER:
        raise WLException(403, "no access to cancel the invite")

    if not invite_obj.i_status == i_status_choice.STARTED:
        raise WLException(403, "can't cancel invite in this status")

    # if reason_id == 1, the reason must be filled
    if reason_id == 1 and reason == None:
        raise WLException(405, "need a reason")
    invite_obj.reason_class_id = reason_id
    invite_obj.reason = reason if reason_id == 1 else invite_obj.reason_class.reason
    invite_obj.i_status = i_status_choice.CANCELED
    invite_obj.save()
    return invite_obj
