from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error500, Error404, WLException, default_exception
from usersys.models import UserBase
from appraisalsys.models import AppraisalInfo
from simplified_invite.model_choices.invite_enum import i_status_choice
from simplified_invite.models import InviteInfo
from appraisalsys.model_choices.appraisal_enum import a_status_choice
from usersys.model_choices.user_enum import role_choice


@default_exception(Error500)
@user_from_sid(Error404)
def submit_appraisal(user, ivid, parameter):
    # type: (UserBase, int, dict) -> QuerySet
    try:
        iv_obj = InviteInfo.objects.get(id=ivid)
    except InviteInfo.DoesNotExist:
        raise WLException(404, "no such ivid")

    if not user.role == role_choice.BUYER or not user == iv_obj.uid_s:
        raise WLException(403, 'this user has no access to submit the invite')

    if not iv_obj.i_status == i_status_choice.STARTED:
        raise WLException(403, 'invite in this status can not submit aappraisal')

    iv_obj.i_status = i_status_choice.SIGNED
    iv_obj.save()
    appraisal_obj = AppraisalInfo.objects.create(**parameter)
    appraisal_obj.ivid = iv_obj
    appraisal_obj.a_status = a_status_choice.APPRAISAL_SUBMITTED
    appraisal_obj.save()
    return appraisal_obj

