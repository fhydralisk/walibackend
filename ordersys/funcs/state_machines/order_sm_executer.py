from base.exceptions import WLException
from ordersys.funcs.state_machines.order_sm import order_sm


def execute_order_state_machine(user, order, action, parameter):
    def state_dealer(state_next, **kwargs):
        order.o_status = state_next
        order.save()

    try:
        order_sm.execute_transition(
            order.o_status,
            action,
            {"order": order, "parameter": parameter, "user": user},
            state_dealer
        )
    except order_sm.ActionError:
        raise WLException(403, "Action error")
    except order_sm.StateDoesNotExist:
        raise

