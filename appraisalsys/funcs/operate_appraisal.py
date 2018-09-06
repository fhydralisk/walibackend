# -*- coding: UTF-8 -*-
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error500, Error404, WLException, default_exception
from usersys.models import UserBase
from appraisalsys.models import AppraisalInfo
from simplified_invite.model_choices.invite_enum import i_status_choice
from simplified_invite.models import InviteInfo
from appraisalsys.model_choices.appraisal_enum import a_status_choice
from appraisalsys.models import CheckPhoto
from usersys.model_choices.user_enum import role_choice


@default_exception(Error500)
@user_from_sid(Error404)
def submit_appraisal(user, ivid, in_accordance, parameter, check_photos=None):
    # type: (UserBase, int, bool, dict, list) -> AppraisalInfo
    try:
        iv_obj = InviteInfo.objects.get(id=ivid)
    except InviteInfo.DoesNotExist:
        raise WLException(404, "no such ivid")

    if user.role != role_choice.BUYER or user != iv_obj.uid_s:
        raise WLException(403, 'this user has no access to submit the invite')

    if not iv_obj.i_status == i_status_choice.STARTED:
        raise WLException(403, 'invite in this status can not submit appraisal')

    if in_accordance:
        appraisal_obj = AppraisalInfo.objects.create(
            in_accordance=in_accordance,
            a_status=a_status_choice.APPRAISAL_SUBMITTED,
            ivid=iv_obj,
            final_total_price=iv_obj.price,
            wcid=iv_obj.dmid_t.wcid,
        )

    else:
        appraisal_obj = AppraisalInfo.objects.create(
            in_accordance=in_accordance,
            ivid=iv_obj,
            a_status=a_status_choice.APPRAISAL_SUBMITTED,
            **parameter
        )
    iv_obj.i_status = i_status_choice.SIGNED
    iv_obj.save()

    exc = WLException(400, "invite_photos contains invalid photo id.")
    if check_photos is not None:
        photo_objs = CheckPhoto.objects.select_related('apprid').filter(id__in=check_photos)
        if photo_objs.count() != len(check_photos):
            raise exc

        for photo_obj in photo_objs:
            if photo_obj.uploader != user:
                raise exc
            if photo_obj.apprid is not None:
                raise exc

        photo_objs.update(apprid=appraisal_obj)

    return appraisal_obj
