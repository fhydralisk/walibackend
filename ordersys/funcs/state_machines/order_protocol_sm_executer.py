from base.exceptions import WLException
from .order_protocol_sm import order_protocol_operate_sm
from ordersys.models import OrderProtocol


def execute_order_protocol_state_machine(user, order, action, parameter):
    try:
        protocol = order.current_protocol
    except OrderProtocol.DoesNotExist:
        raise WLException(403, "Protocol does not exist")
    except OrderProtocol.MultipleObjectsReturned:
        raise AssertionError("Multiple processing protocol")

    try:
        state_next = order_protocol_operate_sm.execute_transition(
            protocol.p_operate_status,
            action,
            {"order": order, "protocol": protocol, "parameter": parameter, "user": user}
        )

        protocol.p_operate_status = state_next
        protocol.save()
    except order_protocol_operate_sm.ActionError:
        raise WLException(403, "Action error")
    except order_protocol_operate_sm.StateDoesNotExist:
        raise
