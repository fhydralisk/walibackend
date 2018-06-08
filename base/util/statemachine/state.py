from .side_effect import SideEffectContainer, bind_side_effects
from .exceptions import *


class State(SideEffectContainer):
    KEY_STATE = "state"
    KEY_PRE_TRANSITIONS = "pre_side_effects"
    KEY_POST_TRANSITIONS = "post_side_effects"
    KEY_CONTEXT = "ctx"

    target_states = {}

    def __init__(self, value, *args, **kwargs):
        self.value = value
        super(State, self).__init__(*args, **kwargs)

    def next_state_dict(self, action):
        try:
            return self.target_states[action]
        except KeyError:
            raise ActionError()

    def next_state(self, action):
        return self.next_state_dict(action)[State.KEY_STATE]

    # def init(self, instance, context, raise_transition_exception, deal_state=True):
    #     errors = self.pre_init(instance, context, raise_transition_exception)
    #     if deal_state:
    #         errors += self._deal_state(instance, context)
    #     errors += self.post_init(instance, context, raise_transition_exception)
    #     return errors
    # 
    # def _deal_state(self, instance, context):
    #     context = self._make_ctx(context)
    #     self.deal(instance, context)
    # 
    # def deal(self, instance, context):
    #     raise NotImplementedError

    def pre_transit(self, instance, action, context, raise_transition_exception):
        self._action_transit(instance, action, context, raise_transition_exception, True)

    def post_transit(self, instance, action, context, raise_transition_exception):
        self._action_transit(instance, action, context, raise_transition_exception, False)

    def _action_transit(self, instance, action, context, raise_transition_exception, pre):
        if pre:
            key = State.KEY_PRE_TRANSITIONS
        else:
            key = State.KEY_POST_TRANSITIONS

        next_state_dict = self.next_state_dict(action)
        
        # Merge State to State level contexts
        context = dict(next_state_dict[State.KEY_CONTEXT], **context)
        
        return self._run_side_effects(
            next_state_dict[key],
            instance,
            context,
            self,
            next_state_dict[State.KEY_STATE],
            raise_transition_exception
        )

    def set_next_state(self, action, state_next, pre_side_effects=None, post_side_effects=None, ctx=None):
        self.target_states[action] = {}

        if not isinstance(state_next, State):
            raise TypeError("state_next must be State instance.")

        self.target_states[action][State.KEY_STATE] = state_next
        
        state_next_dict = self.next_state_dict(action)

        bind_side_effects(state_next_dict, pre_side_effects, post_side_effects, ctx, True)
