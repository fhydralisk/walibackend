from django.db.models import Q
from base.exceptions import default_exception, Error500
from base.util.pages import get_page_info
from usersys.funcs.utils.usersid import user_from_sid
from ordersys.models import OrderInfo
from ordersys.model_choices.order_enum import order_type_choice, o_status_choice
from usersys.models import UserBase
from ordersys.funcs.placeholder2exceptions import get_placeholder2exception


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("order/info/list/ : user_sid error"))
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
        raise get_placeholder2exception("order/info/list/ : order_type error")

    start, end, n_pages = get_page_info(qs, count_pre_page, page,
                                        index_error_excepiton=get_placeholder2exception("order/info/list/ : page out of range"))

    return qs.order_by("-id")[start:end], n_pages


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("order/info/order/ : user_sid error"))
def obtain_order_detail(user, oid):
    try:
        order = OrderInfo.objects.filter(id=oid).get(Q(ivid__uid_s=user) | Q(ivid__uid_t=user))
    except OrderInfo.DoesNotExist:
        raise get_placeholder2exception("order/info/order/ : no such order")

    return order
