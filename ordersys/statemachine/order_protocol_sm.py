import ordersys.model_choices.order_enum as order_enum
import ordersys.statemachine.order_protocol_se as order_protocol_se

from paymentsys.model_choices.receipt_enum import receipt_type_choice
from ordersys.model_choices.distribution_enum import l_type_choice
from base.util.statemachine import ActionBasedStateMachineDef, SideEffect, State

# se_earnest_refund = SideEffect(
#     "earnest refund",
#     ctx={"r_type": receipt_type_choice.EARNEST_REFUND},
#     handler=order_protocol_se.create_register_receipt
# )

se_pay_final = SideEffect(
    "final payment",
    ctx={
        "r_type": receipt_type_choice.FINAL_PAYMENT,
     },
    handler=order_protocol_se.create_register_receipt
)

se_protocol_finish = SideEffect(
    "protocol finished",
    handler=order_protocol_se.order_protocol_finished
)

se_append_logistics = SideEffect(
    "append logistics info",
    handler=order_protocol_se.append_order_logistics_info,
    ctx={
        "l_type": l_type_choice.RETURN
    }
)


class OrderProtocolStateMachineDef(ActionBasedStateMachineDef):
    cancel_wait_return = State(order_enum.p_operate_status_choice.CANCEL_WAIT_RETURN)
    cancel_wait_confirm = State(order_enum.p_operate_status_choice.CANCEL_WAIT_CONFIRM)
    cancel_wait_refund = State(
        order_enum.p_operate_status_choice.CANCEL_WAIT_REFUND,
        # post_side_effects=[
        #     se_earnest_refund
        # ]
    )
    cancel_OK = State(
        order_enum.p_operate_status_choice.CANCEL_OK,
        post_side_effects=[
            se_protocol_finish
        ],
        ctx={
            "action": order_enum.opf_feedback_choice.CANCEL_FINISH
        }
    )

    adjust_wait_final = State(order_enum.p_operate_status_choice.ADJUST_WAIT_FINAL)
    adjust_check_final = State(order_enum.p_operate_status_choice.ADJUST_CHECK_FINAL)
    # adjust_check_earnest = State(
    #     order_enum.p_operate_status_choice.ADJUST_CHECK_EARNEST,
    #     pre_side_effects=[
    #         se_earnest_refund
    #     ],
    #     ctx={
    #         "with_adjustment": True
    #     }
    # )
    adjust_ok = State(
        order_enum.p_operate_status_choice.ADJUST_OK,
        post_side_effects=[
            se_protocol_finish
        ],
        ctx={
            "action": order_enum.opf_feedback_choice.ADJUST_FINISH
        }
    )

    normal_wait_final = State(order_enum.p_operate_status_choice.NORMAL_WAIT_FINAL)
    normal_check_final = State(order_enum.p_operate_status_choice.NORMAL_CHECK_FINAL)
    normal_ok = State(
        order_enum.p_operate_status_choice.NORMAL_OK,
        post_side_effects=[
            se_protocol_finish
        ],
        ctx={
            "action": order_enum.opf_feedback_choice.NORMAL_FINISH
        }
    )

    # Cancel protocol
    cancel_wait_return.set_next_state(
        order_enum.op_buyer_action_choice.CANCEL_APPEND_LOGISTICS_INFO,
        cancel_wait_confirm,
        pre_side_effects=[
            se_append_logistics
        ]
    )

    cancel_wait_confirm.set_next_state(
        order_enum.op_seller_action_choice.CANCEL_CONFIRM_PRODUCT,
        cancel_wait_refund
    )

    cancel_wait_refund.set_next_state(
        order_enum.op_platform_action_choice.PLATFORM_CONFIRM_REFUND,
        cancel_OK
    )

    # adjust protocol
    adjust_wait_final.set_next_state(
        order_enum.op_buyer_action_choice.BUYER_PAY_FINAL,
        adjust_wait_final,
        post_side_effects=[
            se_pay_final
        ],
        ctx={
            "with_adjustment": True
        }
    )

    adjust_check_final.set_next_state(
        order_enum.op_platform_action_choice.PLATFORM_CONFIRM_PAYMENT,
        adjust_ok,
    )

    # adjust_check_earnest.set_next_state(
    #     order_enum.op_platform_action_choice.PLATFORM_CONFIRM_REFUND,
    #     adjust_ok,
    # )

    # normal protocol
    normal_wait_final.set_next_state(
        order_enum.op_buyer_action_choice.BUYER_PAY_FINAL,
        normal_check_final,
        post_side_effects=[
            se_pay_final
        ]
    )

    normal_check_final.set_next_state(
        order_enum.op_platform_action_choice.PLATFORM_CONFIRM_PAYMENT,
        normal_ok,
    )

    def transit_done_dealer(self, instance, context, state_current, state_next, raise_side_effect_exception):
        if state_current != state_next:
            instance.save()

        return []
