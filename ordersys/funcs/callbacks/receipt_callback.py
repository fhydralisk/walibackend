from paymentsys.funcs.receipt_manager import AbstractReceiptCallback
from ordersys.funcs.state_machines.order_sm_executer import execute_order_state_machine
from ordersys.funcs.state_machines.order_protocol_sm_executer import execute_order_protocol_state_machine
from ordersys.model_choices.order_enum import op_platform_action_choice, o_status_choice
from ordersys.models import OrderInfo


class SimpleReceiptCallback(AbstractReceiptCallback):

    def pay_confirm(self, order, context):
        # type: (OrderInfo, dict) -> None
        if order.o_status in (o_status_choice.WAIT_DEFAULT_ADJUSTMENT_COMPLETE, o_status_choice.WAIT_ADJUSTMENT_COMPLETE):
            execute_order_protocol_state_machine(None, order, op_platform_action_choice.PLATFORM_CONFIRM_PAYMENT, None)

    def refund_confirm(self, order, context):
        # type: (OrderInfo, dict) -> None
        if order.o_status in (o_status_choice.WAIT_DEFAULT_ADJUSTMENT_COMPLETE, o_status_choice.WAIT_ADJUSTMENT_COMPLETE):
            execute_order_protocol_state_machine(None, order, op_platform_action_choice.PLATFORM_CONFIRM_REFUND, None)


simple_receipt_callback = SimpleReceiptCallback()
