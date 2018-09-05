from base.util.pages import get_page_info
from base.exceptions import Error500, Error404, WLException, default_exception
from usersys.models import UserBase, UserValidateArea
from usersys.model_choices.user_enum import role_choice
from usersys.funcs.utils.usersid import user_from_sid
from demandsys.models import ProductDemand
from simplified_invite.models import InviteInfo
from simplified_invite.model_choices.invite_enum import t_invite_choice, i_status_choice
from django.db.models import Q



@default_exception(Error500)
@user_from_sid(Error404)
def demand_to_invite(user, dmid):
    # type: (UserBase, int) -> dict
    if not user.role == role_choice.BUYER:
        raise WLException(403, "only buyer can operate")
    try:
        demand = ProductDemand.objects.get(id=dmid, in_use=True)
    except ProductDemand.DoesNotExist:
        raise WLException(404, "no such dmid")
    if not demand.uid.role == role_choice.SELLER:
        raise WLException(403, "only demand of seller can be operated")
    validate_area = UserValidateArea.objects.filter(vid__uid=user).last()
    invite = {
        "price": demand.price,
        "quantity": demand.quantity,
        "aid": None if validate_area == None else validate_area.aid,
        "street": None if user.user_validate.address == None else user.user_validate.address
    }
    return invite


@default_exception(Error500)
@user_from_sid(Error404)
def obtain_self_invite2appraisal_list(count_per_page, user, page, t_invite):
    # type: (int, UserBase, int, int) -> Queryset
    qs = user.simplified_user_invite_dst.all() | user.simplified_user_invite_src.all()
    if t_invite == t_invite_choice.PROCEEDING:
        qs = qs.filter(i_status=i_status_choice.STARTED)
    elif t_invite == t_invite_choice.COMPLETED_OR_CANCELED:
        qs = qs.filter(Q(i_status=i_status_choice.CANCELED) | Q(i_status=i_status_choice.SIGNED))
    else:
        raise WLException(400, "this type is invalid")
    start, end, n_pages = get_page_info(
        qs, count_per_page, page, index_error_excepiton=WLException(400, "Page out of range")
    )
    return qs.order_by("-id")[start:end], n_pages

@default_exception(Error500)
@user_from_sid(Error404)
def obtain_invite2appraisal_detail(user, ivid):
    # type: (UserBase, int) -> Queryset
    try:
        iv = InviteInfo.objects.get(id=ivid)
    except InviteInfo.DoesNotExist:
        raise WLException(404, "No such invite")

    if not (user == iv.uid_s or user == iv.uid_t):
        raise WLException(403, "no access to obtain this invite")

    return iv
