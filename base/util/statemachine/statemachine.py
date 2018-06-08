from inspect import getmembers
from .state import State
from .side_effect import SideEffectContainer
from .exceptions import *


class ActionBasedStateMachineDef(SideEffectContainer):

    attr = None
    
    def __init__(self, attr=None, *args, **kwargs):
        if attr is not None:
            self.attr = attr

        if not isinstance(self.attr, (str, unicode)):
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
        
        # context = dict(self.ctx, **context)
        inner_ctx = self.ctx

        kwargs = {
            "instance": instance,
            "inner_ctx": inner_ctx,
            "context": context,
            "raise_side_effect_exception": raise_side_effect_exception,
        }
        kwargs_deal = dict({
            "state_current": self._get_state(instance),
            "state_next": next_state
        }, **kwargs)

        errors = []
        e, c = self.pre_init(**kwargs_deal)
        errors += e
        if not c:
            return errors

        e, c = state.pre_transit(action=action, **kwargs)
        errors += e
        if not c:
            return errors

        e, c = next_state.pre_init(**kwargs_deal)
        errors += e
        if not c:
            return errors

        setattr(instance, self.attr, next_state.value)
        if deal_state:
            self._transit_done_dealer(**kwargs_deal)

        e, c = next_state.post_init(**kwargs_deal)
        errors += e
        if not c:
            return errors

        e, c = state.post_transit(action=action, **kwargs)
        errors += e
        if not c:
            return errors

        e, c = self.post_init(**kwargs_deal)
        errors += e
        return errors

    def _transit_done_dealer(self, instance, inner_ctx, context, state_current, state_next, raise_side_effect_exception):
        context = dict(inner_ctx, **context)
        return self.transit_done_dealer(instance, context, state_current, state_next, raise_side_effect_exception)
    
    def transit_done_dealer(self, instance, context, state_current, state_next, raise_side_effect_exception):
        raise NotImplementedError

    def init_sm(self, instance, context, raise_side_effect_exception=False, deal_state=False):
        state = self._get_state(instance)
        inner_ctx = self.ctx

        kwargs = {
            "instance": instance,
            "context": context,
            "inner_ctx": inner_ctx,
            "raise_side_effect_exception": raise_side_effect_exception,
            "state_current": self._get_state(instance),
            "state_next": self._get_state(instance),
        }

        errors = []
        e, c = self.pre_init(**kwargs)
        errors += e
        if not c:
            return errors

        e, c = state.pre_init(**kwargs)
        errors += e
        if not c:
            return errors

        if deal_state:
            self.transit_done_dealer(**kwargs)

        e, c = state.post_init(**kwargs)
        errors += e
        if not c:
            return errors

        e, c = self.post_init(**kwargs)
        errors += e
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

    def execute_transition(self, attr, action, context=None, raise_side_effect_exception=False, deal_state=True):
        if context is None:
            context = {}

        sm = self._get_sm(attr)
        return sm.execute_transition(self, action, context, raise_side_effect_exception, deal_state)

    def init_sm(self, attr, context=None, raise_side_effect_exception=False, deal_state=False):
        if context is None:
            context = {}

        sm = self._get_sm(attr)
        return sm.init_sm(self, context, raise_side_effect_exception, deal_state)
