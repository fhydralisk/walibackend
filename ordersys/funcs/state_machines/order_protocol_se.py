from base.exceptions import WLException
from ordersys.models.order_enum import p_status_choice
from ordersys.funcs.state_machines.order_sm_executer import execute_order_state_machine


def order_protocol_finished(extra_ctx, ctx, **kwargs):

    order = extra_ctx["order"]
    if "protocol" in extra_ctx:
        protocol = extra_ctx["protocol"]
    else:
        protocol = order.current_protocol

    if protocol.p_status != p_status_choice.AGREED:
        raise WLException(403, "Cannot finish protocol of status %d." % protocol.p_status)

    protocol.p_status = p_status_choice.EXECUTED
    protocol.save()

    execute_order_state_machine(
        extra_ctx.get("user", None),
        order,
        ctx["action"],
        None
    )

