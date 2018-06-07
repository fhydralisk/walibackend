from inspect import getmembers
from .state import State
from .side_effect import SideEffectContainer
from .exceptions import *


class ActionBasedStateMachineDef(SideEffectContainer):

    attr = None
    
    def __init__(self, attr=None, *args, **kwargs):
        if self.attr is not None:
            self.attr = attr

        if not isinstance(self.attr, str):
            raise AssertionError('attr is not String but %s' % str(self.attr.__class__))

        self.state_map = {s.value: s for s in self._get_states()}
        super(ActionBasedStateMachineDef, self).__init__(*args, **kwargs)

    @classmethod
    def _get_states(cls):
        return [state for _, state in getmembers(cls, lambda x: isinstance(x, State))]

    def _get_state(self, instance):
        if not hasattr(instance, self.attr):
            raise AttributeError("Instance %s does not have attribute %s" % (str(instance), self.attr))

        try:
            return self.state_map[getattr(instance, self.attr)]
        except KeyError:
            raise StateError()

    def execute_transition(self, instance, action, context, raise_side_effect_exception=False, deal_state=True):
        state = self._get_state(instance)
        next_state = state.next_state(action=action)  # type: State
        
        context = dict(self.ctx, **context)
        kwargs = {
            "instance": instance,
            "context": context,
            "raise_side_effect_exception": raise_side_effect_exception,
            "state_current": self._get_state(instance),
            "state_next": next_state
        }

        errors = []
        errors += self.pre_init(**kwargs)
        errors += state.pre_transit(action=action, **kwargs)
        errors += next_state.pre_init(**kwargs)
        setattr(instance, self.attr, next_state.value)
        if deal_state:
            self.transit_done_dealer(**kwargs)
        errors += next_state.post_init(**kwargs)
        errors += state.post_transit(action=action, **kwargs)
        errors += self.post_init(**kwargs)
        return errors
    
    def transit_done_dealer(self, instance, context, state_current, state_next, raise_transition_exception):
        raise NotImplementedError

    def init_sm(self, instance, context, raise_side_effect_exception=False, deal_state=False):
        state = self._get_state(instance)
        kwargs = {
            "instance": instance,
            "context": context,
            "raise_side_effect_exception": raise_side_effect_exception,
            "state_current": self._get_state(instance),
            "state_next": self._get_state(instance),
        }

        errors = []
        errors += self.pre_init(**kwargs)
        errors += state.pre_init(**kwargs)
        if deal_state:
            self.transit_done_dealer(**kwargs)
        errors += state.post_init(**kwargs)
        errors += self.post_init(**kwargs)
        return errors


class ActionBasedStateMachineMixin(object):
    def __init__(self):
        self.attr_sm_map = {
            smdef.attr: smdef for smdef in self._get_sm_defs()
        }

    @classmethod
    def _get_sm_defs(cls):
        return [sm_def for _, sm_def in getmembers(cls, lambda x: isinstance(x, ActionBasedStateMachineDef))]

    def _get_sm(self, attr):
        # type: (str) -> ActionBasedStateMachineDef
        if attr not in self.attr_sm_map:
            raise KeyError("not a valid attr")

        return self.attr_sm_map[attr]

    def execute_transition(self, attr, action, context, raise_side_effect_exception=False, deal_state=True):

        sm = self._get_sm(attr)
        return sm.execute_transition(self, action, context, raise_side_effect_exception, deal_state)

    def init_sm(self, attr, context, raise_side_effect_exception=False, deal_state=False):

        sm = self._get_sm(attr)
        return sm.init_sm(self, context, raise_side_effect_exception, deal_state)
