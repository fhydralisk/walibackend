from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error500, Error404, WLException, default_exception
from usersys.models import UserBase
from appraisalsys.models import AppraisalInfo
from appraisalsys.model_choices.appraisal_enum import t_appraisal_choice, a_status_choice
from simplified_invite.model_choices.invite_enum import i_status_choice
from base.util.pages import get_page_info


@default_exception(Error500)
@user_from_sid(Error404)
def obtain_self_appraisal_list(count_per_page, user, page, t_appraisal):
    # type: (int, UserBase, int, int) -> Queryset
    qs = AppraisalInfo.objects.filter(ivid__in=(user.user_invite_src.all() | user.user_invite_dst.all()))
    if t_appraisal == t_appraisal_choice.PROCEEDING:
        qs = qs.filter(a_status=a_status_choice.WAIT_APPRAISAL).filter(ivid__i_status=i_status_choice.STARTED)
    if t_appraisal_choice == t_appraisal_choice.CANCELED:
        qs = qs.filter(a_status=a_status_choice.WAIT_APPRAISAL).filter(ivid__i_status=i_status_choice.CANCELED)
    if t_appraisal_choice == t_appraisal_choice.COMPLETED:
        qs = qs.exclude(a_status=a_status_choice.WAIT_APPRAISAL)
    else:
        raise WLException(400, "other type is invalid")

    start, end, n_pages = get_page_info(qs, count_per_page, page,
                                        index_error_excepiton=WLException(400, "Page out of range"))
    return qs.order_by("-id")[start:end], n_pages


@default_exception(Error500)
@user_from_sid(Error404)
def obtain_appraisal_detail(user, apprid):
    # type: (UserBase, int) -> Queryset
    try:
        appraisal = AppraisalInfo.objects.get(id=apprid)
    except AppraisalInfo.DoesNotExist:
        raise WLException(404, "No such appraisal")

    if not (user == appraisal.ivid.uid_s or user == appraisal.ivid.uid_t):
        raise WLException(403, "no access to obtain this appraisal")

    return appraisal
