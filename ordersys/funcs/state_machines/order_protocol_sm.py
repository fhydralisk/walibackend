from base.util.state_machine import StateMachine
from ordersys.models.order_enum import (
    p_operate_status_choice, op_buyer_action_choice,
    op_seller_action_choice, opf_feedback_choice,
    op_platform_action_choice
)
from ordersys.models.distribution_enum import l_type_choice
from paymentsys.models.receipt_enum import receipt_type_choice
from ordersys.funcs.state_machines.distribution_se import append_order_logistics_info
import order_protocol_se
from ordersys.funcs.state_machines import order_se


class OrderProtocolOperateStateMachine(StateMachine):
    STATE_MACHINE_DEFINE = {
        StateMachine.K_STATE_GRAPH: {
            p_operate_status_choice.CANCEL_WAIT_RETURN: {
                StateMachine.K_TRANSITIONS: {
                    op_buyer_action_choice.CANCEL_APPEND_LOGISTICS_INFO: {
                        StateMachine.K_NEXT_STATE: p_operate_status_choice.CANCEL_WAIT_CONFIRM,
                        StateMachine.K_PRE_SE: [
                            append_order_logistics_info,
                        ],
                        StateMachine.K_SE_CONTEXT: {
                            "l_type": l_type_choice.RETURN
                        }
                    }
                }
            },
            p_operate_status_choice.CANCEL_WAIT_CONFIRM: {
                StateMachine.K_TRANSITIONS: {
                    op_seller_action_choice.CANCEL_CONFIRM_PRODUCT: {
                        StateMachine.K_NEXT_STATE: p_operate_status_choice.CANCEL_WAIT_REFUND,
                        StateMachine.K_PRE_SE: []
                    }
                }
            },
            p_operate_status_choice.CANCEL_WAIT_REFUND: {
                StateMachine.K_POST_SE: [
                    order_se.create_register_receipt
                ],
                StateMachine.K_SE_CONTEXT: {
                    "r_type": receipt_type_choice.EARNEST_REFUND
                },
                StateMachine.K_TRANSITIONS: {
                    op_platform_action_choice.PLATFORM_CONFIRM_REFUND: {
                        StateMachine.K_NEXT_STATE: p_operate_status_choice.CANCEL_OK,
                    }
                }
            },
            p_operate_status_choice.CANCEL_OK: {
                StateMachine.K_POST_SE: [
                    order_protocol_se.order_protocol_finished,
                ],
                StateMachine.K_SE_CONTEXT: {
                    "action": opf_feedback_choice.CANCEL_FINISH
                }
            },

            p_operate_status_choice.ADJUST_WAIT_FINAL: {
                StateMachine.K_TRANSITIONS: {
                    op_buyer_action_choice.BUYER_PAY_FINAL: {
                        StateMachine.K_NEXT_STATE: p_operate_status_choice.ADJUST_CHECK_FINAL,
                        StateMachine.K_POST_SE: [
                            order_se.create_register_receipt
                        ],
                        StateMachine.K_SE_CONTEXT: {
                            "r_type": receipt_type_choice.FINAL_PAYMENT,
                            "with_adjustment": True
                        }
                    }
                }
            },
            p_operate_status_choice.ADJUST_CHECK_FINAL: {
                StateMachine.K_TRANSITIONS: {
                    op_platform_action_choice.PLATFORM_CONFIRM_PAYMENT: {
                        StateMachine.K_NEXT_STATE: p_operate_status_choice.ADJUST_OK,
                        StateMachine.K_PRE_SE: [],
                    },
                }
            },
            p_operate_status_choice.ADJUST_CHECK_EARNEST: {
                StateMachine.K_PRE_SE: [
                    order_se.create_register_receipt
                ],
                StateMachine.K_SE_CONTEXT: {
                    "r_type": receipt_type_choice.EARNEST_REFUND,
                    "with_adjustment": True
                },
                StateMachine.K_TRANSITIONS: {
                    op_platform_action_choice.PLATFORM_CONFIRM_REFUND: {
                        StateMachine.K_NEXT_STATE: p_operate_status_choice.ADJUST_OK,
                    },
                }
            },
            p_operate_status_choice.ADJUST_OK: {
                StateMachine.K_POST_SE: [
                    order_protocol_se.order_protocol_finished,
                ],
                StateMachine.K_SE_CONTEXT: {
                    "action": opf_feedback_choice.ADJUST_FINISH
                }
            },

            p_operate_status_choice.NORMAL_WAIT_FINAL: {
                StateMachine.K_TRANSITIONS: {
                    op_platform_action_choice.PLATFORM_CONFIRM_PAYMENT: {
                        StateMachine.K_NEXT_STATE: p_operate_status_choice.NORMAL_OK,
                        StateMachine.K_PRE_SE: [],
                    },
                    op_buyer_action_choice.BUYER_PAY_FINAL: {
                        StateMachine.K_NEXT_STATE: p_operate_status_choice.NORMAL_CHECK_FINAL,
                        StateMachine.K_PRE_SE: [],
                    }
                }
            },
            p_operate_status_choice.NORMAL_CHECK_FINAL: {
                StateMachine.K_TRANSITIONS: {
                    op_platform_action_choice.PLATFORM_CONFIRM_PAYMENT: {
                        StateMachine.K_NEXT_STATE: p_operate_status_choice.NORMAL_OK,
                    },
                }
            },
            p_operate_status_choice.NORMAL_OK: {
                StateMachine.K_POST_SE: [
                    order_protocol_se.order_protocol_finished,
                ],
                StateMachine.K_SE_CONTEXT: {
                    "action": opf_feedback_choice.NORMAL_FINISH
                }
            },

        }
    }


order_protocol_operate_sm = OrderProtocolOperateStateMachine()
