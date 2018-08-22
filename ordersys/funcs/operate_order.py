from base.exceptions import default_exception, Error500
from usersys.funcs.utils.usersid import user_from_sid
from usersys.model_choices.user_enum import role_choice
from ordersys.models import OrderInfo
from invitesys.models import InviteInfo
from ordersys.model_choices.order_enum import (
    o_buyer_action_choice, o_seller_action_choice,
    op_buyer_action_choice, op_seller_action_choice,
    o_status_choice
)
from ordersys.funcs.state_machines.order_sm_executer import execute_order_state_machine
from ordersys.funcs.state_machines.order_protocol_sm_executer import execute_order_protocol_state_machine
from base.util.placeholder2exceptions import get_placeholder2exception

def create_order(operator, invite):
    # type: (InviteInfo) -> None
    o_status = o_status_choice.WAIT_EARNEST if invite.earnest > 0 else o_status_choice.WAIT_PRODUCT_DELIVER
    new_order = OrderInfo(ivid=invite, o_status=o_status)
    new_order.operator = operator
    new_order.save()


def operate_order_role(user, oid, action, parameter):
    try:
        order = OrderInfo.objects.select_related("ivid__uid_s", "ivid__uid_t").get(id=oid)
        if (user.role == role_choice.SELLER and order.ivid.seller != user) \
                or (user.role == role_choice.BUYER and order.ivid.buyer != user):
            raise OrderInfo.DoesNotExist
    except OrderInfo.DoesNotExist:
        raise get_placeholder2exception("order/operate/order/ : no such oid")

    execute_order_state_machine(user, order, action, parameter)
    return order


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("order/operate/order/ : user_sid_error"))
def operate_order(user, oid, action, parameter=None):
    if user.role == role_choice.BUYER:
        if action not in o_buyer_action_choice.get_choices():
            raise get_placeholder2exception("order/operate/order/ : invalid action of buyer")

    elif user.role == role_choice.SELLER:
        if action not in o_seller_action_choice.get_choices():
            raise get_placeholder2exception("order/operate/order/ : invalid action of seller")
    else:
        raise get_placeholder2exception("order/operate/order/ : invalid user")

    return operate_order_role(user, oid, action, parameter)


def operate_order_protocol_role(user, oid, action, parameter):
    try:
        order = OrderInfo.objects.select_related("ivid__uid_s", "ivid__uid_t").get(id=oid)
        if (user.role == role_choice.SELLER and order.ivid.seller != user)\
                or (user.role == role_choice.BUYER and order.ivid.buyer != user):

            raise OrderInfo.DoesNotExist
    except OrderInfo.DoesNotExist:
        raise get_placeholder2exception("order/operate/photocol/ : no such oid")

    execute_order_protocol_state_machine(user, order, action, parameter)
    return order


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("order/operate/photocol/ : user_sid error"))
def operate_order_protocol(user, oid, action, parameter):
    if user.role == role_choice.BUYER:
        if action not in op_buyer_action_choice.get_choices():
            raise get_placeholder2exception("order/operate/photocol/ : invalid action of buyer")

    elif user.role == role_choice.SELLER:
        if action not in op_seller_action_choice.get_choices():
            raise get_placeholder2exception("order/operate/photocol/ : invalid action of seller")

    else:
        raise get_placeholder2exception("order/operate/photocol/ : invalid user")

    return operate_order_protocol_role(user, oid, action, parameter)
