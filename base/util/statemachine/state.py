from .side_effect import SideEffectContainer, bind_side_effects
from .exceptions import *


class State(SideEffectContainer):
    KEY_STATE = "state"
    KEY_PRE_TRANSITIONS = "pre_side_effects"
    KEY_POST_TRANSITIONS = "post_side_effects"
    KEY_CONTEXT = "ctx"

    def __init__(self, value, *args, **kwargs):
        self.value = value
        self.target_states = {}
        super(State, self).__init__(*args, **kwargs)

    def next_state_dict(self, action):
        try:
            return self.target_states[action]
        except KeyError:
            raise ActionError()

    def next_state(self, action):
        return self.next_state_dict(action)[State.KEY_STATE]

    def pre_transit(self, instance, action, inner_ctx, context, raise_side_effect_exception):
        return self._action_transit(instance, action, inner_ctx, context, raise_side_effect_exception, True)

    def post_transit(self, instance, action, inner_ctx, context, raise_side_effect_exception):
        return self._action_transit(instance, action, inner_ctx, context, raise_side_effect_exception, False)

    def _action_transit(self, instance, action, inner_ctx, context, raise_side_effect_exception, pre):
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
            inner_ctx,
            context,
            self,
            next_state_dict[State.KEY_STATE],
            raise_side_effect_exception
        )

    def set_next_state(self, action, state_next, pre_side_effects=None, post_side_effects=None, ctx=None):
        self.target_states[action] = {}

        if not isinstance(state_next, State):
            raise TypeError("state_next must be State instance.")

        self.target_states[action][State.KEY_STATE] = state_next
        
        state_next_dict = self.next_state_dict(action)

        bind_side_effects(state_next_dict, pre_side_effects, post_side_effects, ctx, True)

    def __repr__(self):
        return "State %s at 0x%X" % (str(self.value), id(self))
