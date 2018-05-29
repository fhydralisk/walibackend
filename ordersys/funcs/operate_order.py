from base.exceptions import WLException, default_exception, Error500, Error404
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


def create_order(invite):
    # type: (InviteInfo) -> None
    o_status = o_status_choice.WAIT_EARNEST if invite.earnest > 0 else o_status_choice.WAIT_PRODUCT_DELIVER
    new_order = OrderInfo(ivid=invite, o_status=o_status)
    new_order.save()


def operate_order_role(user, oid, action, parameter):
    try:
        order = OrderInfo.objects.select_related("ivid__uid_s", "ivid__uid_t").get(id=oid)
        if (user.role == role_choice.SELLER and order.ivid.seller != user) \
                or (user.role == role_choice.BUYER and order.ivid.buyer != user):
            raise OrderInfo.DoesNotExist
    except OrderInfo.DoesNotExist:
        raise WLException(404, "No such oid")

    execute_order_state_machine(user, order, action, parameter)
    return order


@default_exception(Error500)
@user_from_sid(Error404)
def operate_order(user, oid, action, parameter=None):
    if user.role == role_choice.BUYER:
        if action not in o_buyer_action_choice.get_choices():
            raise WLException(403, "Invalid action")

    elif user.role == role_choice.SELLER:
        if action not in o_seller_action_choice.get_choices():
            raise WLException(403, "Invalid action")

    else:
        raise WLException(403, "Invalid user")

    return operate_order_role(user, oid, action, parameter)


def operate_order_protocol_role(user, oid, action, parameter):
    try:
        order = OrderInfo.objects.select_related("ivid__uid_s", "ivid__uid_t").get(id=oid)
        if (user.role == role_choice.SELLER and order.ivid.seller != user)\
                or (user.role == role_choice.BUYER and order.ivid.buyer != user):

            raise OrderInfo.DoesNotExist
    except OrderInfo.DoesNotExist:
        raise WLException(404, "No such oid")

    execute_order_protocol_state_machine(user, order, action, parameter)


@default_exception(Error500)
@user_from_sid(Error404)
def operate_order_protocol(user, oid, action, parameter):
    if user.role == role_choice.BUYER:
        if action not in op_buyer_action_choice.get_choices():
            raise WLException(403, "Invalid action")

    elif user.role == role_choice.SELLER:
        if action not in op_seller_action_choice.get_choices():
            raise WLException(403, "Invalid action")

    else:
        raise WLException(403, "Invalid user")

    operate_order_protocol_role(user, oid, action, parameter)
