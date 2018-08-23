import ordersys.model_choices.order_enum as order_enum
import ordersys.statemachine.order_se as order_se

from paymentsys.model_choices.receipt_enum import receipt_type_choice
from ordersys.model_choices.distribution_enum import l_type_choice
from base.util.statemachine import ActionBasedStateMachineDef, SideEffect, State


# se_create_receipt = SideEffect(
#     "create or change receipt",
#     handler=order_se.create_register_receipt,
#     ctx={"r_type": receipt_type_choice.EARNEST_PAYMENT}
# )

se_append_default_adjustment = SideEffect(
    "append default adjustment",
    handler=order_se.append_default_order_protocol_info
)

se_init_protocol = SideEffect(
    "prepare protocol",
    handler=order_se.init_protocol
)

se_submit_protocol = SideEffect(
    "submit adjustment protocol",
    handler=order_se.append_order_protocol_info
)


def se_agree_reject_protocol(agree):
    return SideEffect(
        "agree or reject protocol",
        handler=order_se.agree_reject_protocol,
        ctx={
            "agree": agree
        }
    )


def se_append_logistics_info(l_type):
    return SideEffect(
        "create or change logistics info",
        handler=order_se.append_order_logistics_info,
        ctx={
            "l_type": l_type
        }
    )


class OrderInfoStateMachinDef(ActionBasedStateMachineDef):
    # wait_earnest = State(order_enum.o_status_choice.WAIT_EARNEST)
    # wait_earnest_check = State(order_enum.o_status_choice.WAIT_EARNEST_CHECK)
    wait_product_deliver = State(order_enum.o_status_choice.WAIT_PRODUCT_DELIVER)
    wait_product_confirm = State(order_enum.o_status_choice.WAIT_PRODUCT_CHECK)
    wait_product_check = State(order_enum.o_status_choice.WAIT_PRODUCT_CHECK)
    wait_adjustment = State(order_enum.o_status_choice.WAIT_ADJUSTMENT)
    wait_adjustment_confirm = State(order_enum.o_status_choice.WAIT_ADJUSTMENT_CONFIRM)
    wait_default_adjustment_complete = State(order_enum.o_status_choice.WAIT_DEFAULT_ADJUSTMENT_COMPLETE)
    wait_adjustment_complete = State(order_enum.o_status_choice.WAIT_ADJUSTMENT_COMPLETE)
    wait_liquidate = State(
        order_enum.o_status_choice.WAIT_LIQUIDATE,
        post_side_effects=[
            SideEffect("liquidate", handler=order_se.do_or_register_liquidation)
        ]
    )
    wait_receipt = State(order_enum.o_status_choice.WAIT_RECEIPT)
    wait_receipt_check = State(order_enum.o_status_choice.WAIT_RECEIPT_CHECK)
    succeed = State(order_enum.o_status_choice.SUCCEEDED)
    closed = State(order_enum.o_status_choice.CLOSED)

    # wait_earnest.set_next_state(
    #     order_enum.o_buyer_action_choice.BUYER_PAY_EARNEST,
    #     wait_earnest_check,
    #     pre_side_effects=[
    #         se_create_receipt
    #     ],
    # )
    #
    # wait_earnest_check.set_next_state(
    #     order_enum.op_platform_action_choice.PLATFORM_CONFIRM_PAYMENT,
    #     wait_product_deliver,
    # )
    # wait_earnest_check.set_next_state(
    #     order_enum.o_buyer_action_choice.BUYER_PAY_EARNEST,
    #     wait_earnest_check,
    #     pre_side_effects=[
    #         se_create_receipt
    #     ]
    # )

    wait_product_deliver.set_next_state(
        order_enum.o_seller_action_choice.SELLER_SUBMIT_LOGISTICS_INFO,
        wait_product_confirm,
        pre_side_effects=[
            se_append_logistics_info(l_type_choice.FORWARD)
        ]
    )

    wait_product_confirm.set_next_state(
        order_enum.o_buyer_action_choice.BUYER_CHECK_PRODUCT,
        wait_product_check
    )
    wait_product_confirm.set_next_state(
        order_enum.o_seller_action_choice.SELLER_SUBMIT_LOGISTICS_INFO,
        wait_product_confirm,
        pre_side_effects=[
            se_append_logistics_info(l_type_choice.FORWARD)
        ]
    )

    wait_product_check.set_next_state(
        order_enum.o_buyer_action_choice.BUYER_CHECK_RESULT_GOOD,
        wait_default_adjustment_complete,
        pre_side_effects=[
            se_append_default_adjustment
        ]
    )
    wait_product_check.set_next_state(
        order_enum.o_buyer_action_choice.BUYER_CHECK_RESULT_BAD,
        wait_adjustment
    )

    wait_adjustment.set_next_state(
        order_enum.o_buyer_action_choice.BUYER_SUBMIT_PROTOCOL,
        wait_adjustment_confirm,
        pre_side_effects=[
            se_submit_protocol
        ]
    ),
    wait_adjustment.set_next_state(
        order_enum.o_buyer_action_choice.BUYER_CHECK_RESULT_GOOD,
        wait_default_adjustment_complete,
        pre_side_effects=[
            se_append_default_adjustment,
            se_init_protocol,
        ]
    )

    wait_adjustment_confirm.set_next_state(
        order_enum.o_seller_action_choice.SELLER_AGREE_PROTOCOL,
        wait_adjustment_complete,
        pre_side_effects=[
            se_agree_reject_protocol(True),
            se_init_protocol
        ]
    )
    wait_adjustment_confirm.set_next_state(
        order_enum.o_seller_action_choice.SELLER_REJECT_PROTOCOL,
        wait_adjustment,
        pre_side_effects=[
            se_agree_reject_protocol(False)
        ]
    )
    wait_adjustment_confirm.set_next_state(
        order_enum.o_buyer_action_choice.BUYER_SUBMIT_PROTOCOL,
        wait_adjustment_confirm,
        pre_side_effects=[
            se_submit_protocol
        ]
    )
    wait_adjustment_confirm.set_next_state(
        order_enum.o_buyer_action_choice.BUYER_CHECK_RESULT_GOOD,
        wait_default_adjustment_complete,
    )

    wait_default_adjustment_complete.set_next_state(
        order_enum.opf_feedback_choice.NORMAL_FINISH,
        wait_liquidate,
    )

    wait_adjustment_complete.set_next_state(
        order_enum.opf_feedback_choice.ADJUST_FINISH,
        wait_liquidate,
    )
    wait_adjustment_complete.set_next_state(
        order_enum.opf_feedback_choice.CANCEL_FINISH,
        closed,
    )
    wait_adjustment_complete.set_next_state(
        order_enum.opf_feedback_choice.NORMAL_FINISH,
        wait_liquidate,
    )

    wait_liquidate.set_next_state(
        order_enum.op_platform_action_choice.PLATFORM_CONFIRM_PAYMENT,
        wait_receipt
    )

    wait_receipt.set_next_state(
        order_enum.o_seller_action_choice.SELLER_APPEND_RECEIPT_LOGISTICS,
        wait_receipt_check,
        pre_side_effects=[
            se_append_logistics_info(l_type_choice.RECEIPT)
        ]
    )

    wait_receipt_check.set_next_state(
        order_enum.o_buyer_action_choice.BUYER_CONFIRMED_RECEIPT,
        succeed,
    )

    def transit_done_dealer(self, instance, context, state_current, state_next, raise_side_effect_exception):
        if state_current != state_next:
            instance.save()

        return []
