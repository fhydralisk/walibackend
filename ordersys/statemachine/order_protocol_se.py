from base.exceptions import WLException
from ordersys.model_choices.order_enum import p_status_choice
from .order_se import (
    create_register_receipt as order_create_register_receipt,
    append_order_logistics_info as _append_order_logistics_info
)


def order_protocol_finished(instance, context, **kwargs):

    order = context.get("order", instance.oid)
    protocol = instance

    if protocol.p_status != p_status_choice.AGREED:
        raise WLException(403, "Cannot finish protocol of status %d." % protocol.p_status)

    protocol.p_status = p_status_choice.EXECUTED
    protocol.save()

    order.execute_transition('o_status', context["action"], context)


def create_register_receipt(instance, context, **kwargs):
    order = context.get("order", instance.oid)
    order_create_register_receipt(order, context=context, **kwargs)


def append_order_logistics_info(instance, context, **kwargs):
    order = context.get("order", instance.oid)
    _append_order_logistics_info(order, context=context, **kwargs)
