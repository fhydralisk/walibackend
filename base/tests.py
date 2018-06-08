from django.test import TestCase

from base.util.statemachine import ActionBasedStateMachineDef, ActionBasedStateMachineMixin, State, SideEffect
from base.util.statemachine.exceptions import *
# Create your tests here.


def se_0_handler(**kwargs):
    print("se0")
    print(kwargs)


def se_1_handler(**kwargs):
    print("se1")
    print(kwargs)


def se_2_handler(**kwargs):
    print("se2")
    print(kwargs)


se_1 = SideEffect(
    "test_se_1",
    ctx={
        "context": "some"
    },
    continue_after_error=False,
    handler=se_1_handler
)

se_2 = SideEffect(
    "test_se_1",
    ctx={
        "context": "some"
    },
    continue_after_error=False,
    handler=se_2_handler
)


class TestStateMachineDef(ActionBasedStateMachineDef):
    state1 = State(1, pre_side_effects=[se_1])
    state2 = State(2, ctx={"tctx": "state ctx"})
    state3 = State(3)

    state1.set_next_state(2, state2, post_side_effects=[se_2])
    state2.set_next_state(1, state1)
    state2.set_next_state(3, state3, pre_side_effects=[se_1])
    state3.set_next_state(1, state1, ctx={"trans": "state3->state1", "tctx": "transition ctx"}, pre_side_effects=[se_1])

    def transit_done_dealer(self, instance, context, state_current, state_next, raise_side_effect_exception):
        print("deal")


class TestModel(ActionBasedStateMachineMixin):
    status = 1
    status_sm = TestStateMachineDef('status', ctx={"tctx": "sm_field ctx"})


class TestStateMachine(TestCase):
    def test_state_machine(self):
        tm = TestModel()
        tm.init_sm('status', {})
        self.assertEqual(tm.status, 1)

        tm.execute_transition('status', 2)
        self.assertEqual(tm.status, 2)

        try:
            tm.execute_transition('status', 2)
        except ActionError:
            pass
        else:
            self.fail("Action must error")

        tm.execute_transition('status', 3)
        self.assertEqual(tm.status, 3)

        tm.execute_transition('status', 1)
        self.assertEqual(tm.status, 1)
