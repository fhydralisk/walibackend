from base.exceptions import WLException
from base.util.serializer_helper import errors_summery
from ordersys.funcs.calculator.liquidation import liquidation_calculator
from ordersys.funcs.calculator.receipt import receipt_calculator
from ordersys.models import OrderInfo, OrderProtocol
from ordersys.model_choices.order_enum import o_status_choice, op_type_choice, p_status_choice, change_type_choice
from ordersys.serializers.order import OrderProtocolSubmitSerializer
from paymentsys.funcs.liquidation_manager import manager as liquidation_manager
from paymentsys.funcs.receipt_manager import manager as receipt_manager
from paymentsys.models import PaymentReceipt
from paymentsys.model_choices.receipt_enum import receipt_status_choice


def do_or_register_liquidation(extra_ctx, state_next, **kwargs):
    order = extra_ctx["order"]  # type: OrderInfo
    if state_next != o_status_choice.WAIT_LIQUIDATE:
        raise AssertionError("Fatal error, registering liquidation without state WAIT_LIQUIDATE")

    amount = liquidation_calculator.cal_order_liquidation_amount(order)

    liquidation_manager.generate(order, amount)


def create_register_receipt(ctx, extra_ctx, **kwargs):
    order = extra_ctx["order"]  # type: OrderInfo
    r_type = ctx["r_type"]
    try:
        current_receipt = order.current_receipt
        if current_receipt.can_not_change():
            raise WLException(403, "Cannot modify receipt with status %d" % current_receipt.receipt_status)
        current_receipt.receipt_status = receipt_status_choice.CANCELED
        current_receipt.save()
    except PaymentReceipt.DoesNotExist:
        pass
    except PaymentReceipt.MultipleObjectsReturned:
        # This should not be happen.
        raise

    amount = receipt_calculator.cal_order_receipt_amount(order, r_type, dict(ctx, **extra_ctx))

    receipt_manager.generate(order, r_type, amount, extra_ctx["parameter"])


def _validate_and_close_existing_protocol(order):
    protocols = OrderProtocol.objects.filter(oid=order)
    # Check if there is a protocol in progress
    all_protocols = protocols.all()
    for p in all_protocols:
        if not p.terminated and p.p_status != p_status_choice.CREATED:
            raise WLException(403, "Cannot change or add order protocol due to unfinished protocol")

    # Cancel all protocols that are not in progress
    for p in all_protocols:
        if p.p_status == p_status_choice.CREATED:
            p.p_status = p_status_choice.CANCELED
            p.save()


def append_order_protocol_info(extra_ctx, **kwargs):
    # Create default protocol, but without initialize it.
    # The initialization is done the same time when seller agree this protocol.
    parameter = extra_ctx["parameter"]
    order = extra_ctx["order"]  # type: OrderInfo
    pseri = OrderProtocolSubmitSerializer(data=parameter["protocol"])
    if not pseri.is_valid():
        raise WLException(400, errors_summery(pseri))

    c_price = None
    if pseri.validated_data["op_type"] == op_type_choice.ADJUST_PRICE:
        if pseri.validated_data["change_type"] == change_type_choice.REFUND_EARNEST:
            if pseri.validated_data["price"] > order.ivid.earnest:
                raise WLException(400, "price must be less than earnest")
            else:
                c_price = order.ivid.earnest - pseri.validated_data["price"]

        elif pseri.validated_data["change_type"] == change_type_choice.ADJUST_FINAL:
            c_price = order.ivid.earnest + pseri.validated_data["price"]
        else:
            raise AssertionError("Unexpected change type.")

    _validate_and_close_existing_protocol(order)

    new_protocol = OrderProtocol()
    new_protocol.op_type = pseri.validated_data["op_type"]
    new_protocol.description = pseri.validated_data["description"]
    new_protocol.c_price = c_price
    new_protocol.oid = order
    new_protocol.p_status = p_status_choice.CREATED
    new_protocol.init_p_operate_status()
    new_protocol.save()


def append_default_order_protocol_info(extra_ctx, **kwargs):
    # Create default protocol, but without initialize it.
    # The initialization is done the same time when seller agree this protocol.
    order = extra_ctx["order"]
    _validate_and_close_existing_protocol(order)

    default_protocol = OrderProtocol()
    default_protocol.oid = order
    default_protocol.p_status = p_status_choice.AGREED
    # TODO: Move default protocol into settings or ctx
    default_protocol.op_type = op_type_choice.NORMAL
    default_protocol.init_p_operate_status()
    default_protocol.save()


def close_existing_protocol(extra_ctx, **kwargs):
    order = extra_ctx["order"]
    _validate_and_close_existing_protocol(order)


def agree_reject_protocol(ctx, extra_ctx, **kwargs):
    if "protocol" in extra_ctx:
        protocol = extra_ctx["protocol"]
    else:
        order = extra_ctx["order"]
        protocol = order.current_protocol

    agree = ctx["agree"]  # type: bool

    if protocol.p_status != p_status_choice.CREATED:
        raise WLException(403, "Cannot agree or reject this protocol of status %d." % protocol.p_status)

    protocol.p_status = p_status_choice.AGREED if agree else p_status_choice.REJECTED
    protocol.save()


def init_protocol(extra_ctx, **kwargs):
    """
    Initialize the protocol, which will create receipt, generate refund receipt and so on.
    :param extra_ctx:
    :param kwargs:
    :return:
    """
    if "protocol" in extra_ctx:
        protocol = extra_ctx["protocol"]
    else:
        order = extra_ctx["order"]
        protocol = order.current_protocol

    if protocol.p_status != p_status_choice.AGREED:
        raise WLException(
            403,
            "Cannot init this protocol of status: %d. Protocol must be agreed to initialize" % protocol.p_status
        )
    # Create receipt, or others...
    from order_protocol_sm import order_protocol_operate_sm
    order_protocol_operate_sm.start_sm(protocol.p_operate_status, extra_ctx, None)

