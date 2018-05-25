from django.db.models import Q
from base.exceptions import WLException, default_exception, Error500, Error404
from base.util.pages import get_page_info
from usersys.funcs.utils.usersid import user_from_sid
from ordersys.models import OrderInfo
from ordersys.models.order_enum import order_type_choice, o_status_choice
from usersys.models import UserBase


@default_exception(Error500)
@user_from_sid(Error404)
def obtain_order_list(user, order_type, page, count_pre_page):
    # type: (UserBase, int, int) -> QuerySet
    qs = OrderInfo.objects.filter(ivid__in=(user.user_invite_dst.all() | user.user_invite_src.all()))
    if order_type == order_type_choice.PROCEEDING:
        qs = qs.exclude(o_status__in=(o_status_choice.CLOSED, o_status_choice.SUCCEEDED))
    elif order_type == order_type_choice.CLOSED:
        qs = qs.filter(o_status=o_status_choice.CLOSED)
    elif order_type == order_type_choice.SUCCEEDED:
        qs = qs.filter(o_status=o_status_choice.SUCCEEDED)
    else:
        raise WLException(400, "order_type is invalid")

    start, end, n_pages = get_page_info(qs, count_pre_page, page,
                                        index_error_excepiton=WLException(400, "Page out of range"))

    return qs.order_by("-id")[start:end], n_pages


@default_exception(Error500)
@user_from_sid(Error404)
def obtain_order_detail(user, oid):
    try:
        order = OrderInfo.objects.filter(id=oid).get(Q(ivid__uid_s=user) | Q(ivid__uid_t=user))
    except OrderInfo.DoesNotExist:
        raise WLException(404, "No such order.")

    return order
