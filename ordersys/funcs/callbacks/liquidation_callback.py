from paymentsys.funcs.liquidation_manager import AbstractLiquidationCallback
from ordersys.models import OrderInfo
from ordersys.model_choices.order_enum import op_platform_action_choice, o_status_choice
from ordersys.funcs.state_machines.order_sm_executer import execute_order_state_machine


class SimpleLiquidationCallback(AbstractLiquidationCallback):
    def confirm_liquidation(self, order, context):
        # type: (OrderInfo, dict) -> None
        if order.o_status == o_status_choice.WAIT_LIQUIDATE:
            execute_order_state_machine(None, order, op_platform_action_choice.PLATFORM_CONFIRM_PAYMENT, None)


simple_liquidation_callback = SimpleLiquidationCallback()
