# -*- coding: UTF-8 -*-
import json
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error500, Error404, WLException, default_exception
from usersys.models import UserBase
from appraisalsys.models import AppraisalInfo, CheckPhoto, JsonSchemaOfAppraisal
from simplified_invite.model_choices.invite_enum import i_status_choice
from simplified_invite.models import InviteInfo
from appraisalsys.model_choices.appraisal_enum import a_status_choice
from usersys.model_choices.user_enum import role_choice
from jsonschema import validate
from jsonschema.exceptions import ValidationError


@default_exception(Error500)
@user_from_sid(Error404)
def submit_appraisal(user, ivid, in_accordance, parameter, check_photos=None):
    # type: (UserBase, int, bool, dict, list) -> AppraisalInfo
    try:
        iv_obj = InviteInfo.objects.select_related('dmid_t__pid__t2id__t1id').get(id=ivid)
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
            net_weight=iv_obj.quantity,
            final_total_price=iv_obj.total_price,
            final_price=iv_obj.price,
            water_content=iv_obj.dmid_t.wcid.water_content,
            tare=0,
            parameter="{}",
        )

    else:
        try:
            parameter_schema = JsonSchemaOfAppraisal.objects.get(t1id=iv_obj.dmid_t.pid.t2id.t1id.id)
            schema = json.loads(parameter_schema.json_schema)
            validate(parameter, schema)
        except JsonSchemaOfAppraisal.DoesNotExist:
            pass
        except ValidationError as e:
            raise WLException(400, str(e.message))

        appraisal_obj = AppraisalInfo(
            in_accordance=in_accordance,
            ivid=iv_obj,
            a_status=a_status_choice.APPRAISAL_SUBMITTED,
            final_price=parameter.pop("final_price"),
            net_weight=parameter.pop("net_weight"),
            water_content=parameter.pop("water_content", None),
            tare=parameter.pop("tare", None),
            deduction_ratio=parameter.pop("deduction_ratio", None),
            parameter=json.dumps(parameter)
        )
        appraisal_obj._history_user = user

        if not ((appraisal_obj.tare is not None) ^ (appraisal_obj.deduction_ratio is not None)):
            raise WLException(400, "One an only one of tare and deduction_ratio field must be filled")

        calculated_weight = \
            appraisal_obj.net_weight - appraisal_obj.tare if appraisal_obj.tare is not None else \
            appraisal_obj.net_weight * (100.0 - appraisal_obj.deduction_ratio) / 100.0

        appraisal_obj.final_total_price = appraisal_obj.final_price * calculated_weight
        appraisal_obj.save()

    iv_obj.i_status = i_status_choice.SIGNED
    iv_obj.save()

    exc = WLException(400, "invite_photos contains invalid photo id.")
    if check_photos is not None:
        photo_objs = CheckPhoto.objects.select_related('apprid').filter(id__in=check_photos)
        if photo_objs.count() != len(check_photos):
            raise exc

        photo_objs.update(in_use=True)

        for photo_obj in photo_objs:
            if photo_obj.uploader != user:
                raise exc
            if photo_obj.apprid is not None:
                raise exc

        photo_objs.update(apprid=appraisal_obj)

    return appraisal_obj
