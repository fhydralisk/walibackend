"""
OrderInfo State Machine


"""

import ordersys.funcs.state_machines.distribution_se
import ordersys.funcs.state_machines.order_se

from base.util.state_machine import StateMachine
from ordersys.model_choices.distribution_enum import l_type_choice
from ordersys.model_choices.order_enum import (
    o_status_choice, o_buyer_action_choice, o_seller_action_choice, opf_feedback_choice, op_platform_action_choice
)
from paymentsys.model_choices.receipt_enum import receipt_type_choice


class OrderInfoStateMachine(StateMachine):
    STATE_MACHINE_DEFINE = {
        StateMachine.K_STATES: o_status_choice.get_choices(),
        StateMachine.K_ACTIONS: (
            o_buyer_action_choice.get_choices() +
            o_seller_action_choice.get_choices() +
            opf_feedback_choice.get_choices() +
            op_platform_action_choice.get_choices()
        ),

        StateMachine.K_STATE_GRAPH: {
            o_status_choice.WAIT_EARNEST: {
                StateMachine.K_TRANSITIONS: {
                    # Wait for earnest payment
                    o_buyer_action_choice.BUYER_PAY_EARNEST: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_EARNEST_CHECK,
                        StateMachine.K_POST_SE: [
                            ordersys.funcs.state_machines.order_se.create_register_receipt
                        ],
                        StateMachine.K_SE_CONTEXT: {
                            "r_type": receipt_type_choice.EARNEST_PAYMENT
                        }
                    }
                }
            },
            o_status_choice.WAIT_EARNEST_CHECK: {
                StateMachine.K_TRANSITIONS: {
                    # TODO: Wait for checking
                    op_platform_action_choice.PLATFORM_CONFIRM_PAYMENT: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_PRODUCT_DELIVER,
                    },
                    o_buyer_action_choice.BUYER_PAY_EARNEST: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_EARNEST_CHECK,
                        StateMachine.K_PRE_SE: [
                            ordersys.funcs.state_machines.order_se.create_register_receipt
                        ],
                        StateMachine.K_SE_CONTEXT: {
                            "r_type": receipt_type_choice.EARNEST_PAYMENT
                        }
                    },
                }
            },
            o_status_choice.WAIT_PRODUCT_DELIVER: {
                StateMachine.K_TRANSITIONS: {
                    o_seller_action_choice.SELLER_SUBMIT_LOGISTICS_INFO: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_PRODUCT_CONFIRM,
                        StateMachine.K_PRE_SE: [
                            ordersys.funcs.state_machines.distribution_se.append_order_logistics_info,
                        ],
                        StateMachine.K_SE_CONTEXT: {
                            "l_type": l_type_choice.FORWARD
                        }
                    }
                    # TODO: Seller close order
                }
            },
            o_status_choice.WAIT_PRODUCT_CONFIRM: {
                StateMachine.K_TRANSITIONS: {
                    o_buyer_action_choice.BUYER_CHECK_PRODUCT: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_PRODUCT_CHECK,
                        StateMachine.K_PRE_SE: []
                    },
                    o_seller_action_choice.SELLER_SUBMIT_LOGISTICS_INFO: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_PRODUCT_CONFIRM,
                        StateMachine.K_PRE_SE: [
                            ordersys.funcs.state_machines.distribution_se.append_order_logistics_info,
                        ],
                        StateMachine.K_SE_CONTEXT: {
                            "l_type": l_type_choice.FORWARD
                        }
                    }
                }
            },
            o_status_choice.WAIT_PRODUCT_CHECK: {
                StateMachine.K_TRANSITIONS: {
                    o_buyer_action_choice.BUYER_CHECK_RESULT_GOOD: {
                        # FIXME: the state is not exactly what it means
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_DEFAULT_ADJUSTMENT_COMPLETE,
                        StateMachine.K_PRE_SE: [
                            ordersys.funcs.state_machines.order_se.append_default_order_protocol_info,
                        ],
                    },
                    o_buyer_action_choice.BUYER_CHECK_RESULT_BAD: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_ADJUSTMENT,
                        StateMachine.K_PRE_SE: []
                    }
                }
            },
            o_status_choice.WAIT_ADJUSTMENT: {
                StateMachine.K_TRANSITIONS: {
                    o_buyer_action_choice.BUYER_SUBMIT_PROTOCOL: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_ADJUSTMENT_CONFIRM,
                        StateMachine.K_PRE_SE: [
                            ordersys.funcs.state_machines.order_se.append_order_protocol_info,
                        ],
                    },
                    o_buyer_action_choice.BUYER_CHECK_RESULT_GOOD: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_DEFAULT_ADJUSTMENT_COMPLETE,
                        StateMachine.K_PRE_SE: [
                            ordersys.funcs.state_machines.order_se.append_default_order_protocol_info,
                            ordersys.funcs.state_machines.order_se.init_protocol,
                        ],
                    }
                }
            },
            o_status_choice.WAIT_ADJUSTMENT_CONFIRM: {
                StateMachine.K_TRANSITIONS: {
                    o_seller_action_choice.SELLER_AGREE_PROTOCOL: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_ADJUSTMENT_COMPLETE,
                        StateMachine.K_PRE_SE: [
                            ordersys.funcs.state_machines.order_se.agree_reject_protocol,
                            ordersys.funcs.state_machines.order_se.init_protocol,
                        ],
                        StateMachine.K_SE_CONTEXT: {
                            "agree": True
                        }
                    },
                    o_seller_action_choice.SELLER_REJECT_PROTOCOL: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_ADJUSTMENT,
                        StateMachine.K_PRE_SE: [
                            ordersys.funcs.state_machines.order_se.agree_reject_protocol
                        ],
                        StateMachine.K_SE_CONTEXT: {
                            "agree": False
                        }
                    },
                    o_buyer_action_choice.BUYER_SUBMIT_PROTOCOL: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_ADJUSTMENT_CONFIRM,
                        StateMachine.K_PRE_SE: [
                            ordersys.funcs.state_machines.order_se.append_order_protocol_info,
                        ]
                    },
                    o_buyer_action_choice.BUYER_CHECK_RESULT_GOOD: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_DEFAULT_ADJUSTMENT_COMPLETE,
                        StateMachine.K_PRE_SE: []
                    }
                }
            },
            o_status_choice.WAIT_DEFAULT_ADJUSTMENT_COMPLETE: {
                StateMachine.K_TRANSITIONS: {
                    # TODO: This transition shall be allowed in future. For now we cannot
                    # deal with the receipt and closing stuff.
                    # o_buyer_action_choice.BUYER_CHECK_RESULT_BAD: {
                    #     StateMachine.K_NEXT_STATE: o_status_choice.WAIT_ADJUSTMENT,
                    #     StateMachine.K_PRE_SE: [
                    #         ordersys.funcs.state_machines.order_se.close_existing_protocol,
                    #     ]
                    # },
                    # OrderProtocol staff.
                    opf_feedback_choice.NORMAL_FINISH: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_LIQUIDATE,
                        StateMachine.K_PRE_SE: []
                    }
                }
            },
            o_status_choice.WAIT_ADJUSTMENT_COMPLETE: {
                StateMachine.K_TRANSITIONS: {
                    # OrderProtocol staff.
                    opf_feedback_choice.ADJUST_FINISH: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_LIQUIDATE,
                        StateMachine.K_PRE_SE: []
                    },
                    opf_feedback_choice.CANCEL_FINISH: {
                        StateMachine.K_NEXT_STATE: o_status_choice.CLOSED,
                        StateMachine.K_PRE_SE: []
                    },
                    opf_feedback_choice.NORMAL_FINISH: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_LIQUIDATE,
                        StateMachine.K_PRE_SE: []
                    }
                }
            },
            o_status_choice.WAIT_LIQUIDATE: {
                StateMachine.K_POST_SE: {
                    ordersys.funcs.state_machines.order_se.do_or_register_liquidation
                },
                StateMachine.K_TRANSITIONS: {
                    op_platform_action_choice.PLATFORM_CONFIRM_PAYMENT: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_RECEIPT,
                        StateMachine.K_PRE_SE: []
                    }
                }
            },
            o_status_choice.WAIT_RECEIPT: {
                StateMachine.K_TRANSITIONS: {
                    o_seller_action_choice.SELLER_APPEND_RECEIPT_LOGISTICS: {
                        StateMachine.K_NEXT_STATE: o_status_choice.WAIT_RECEIPT_CHECK,
                        StateMachine.K_PRE_SE: [
                            ordersys.funcs.state_machines.distribution_se.append_order_logistics_info,
                        ],
                        StateMachine.K_SE_CONTEXT: {
                            "l_type": l_type_choice.RECEIPT
                        }
                    }
                }
            },
            o_status_choice.WAIT_RECEIPT_CHECK: {
                StateMachine.K_TRANSITIONS: {
                    o_buyer_action_choice.BUYER_CONFIRMED_RECEIPT: {
                        StateMachine.K_NEXT_STATE: o_status_choice.SUCCEEDED,
                        StateMachine.K_PRE_SE: []
                    }
                }
            }
        }
    }


order_sm = OrderInfoStateMachine()
