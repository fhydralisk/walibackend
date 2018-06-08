from .exceptions import SideEffectError


Collection = (list, set, tuple)


def bind_side_effects(obj, pre_side_effects, post_side_effects, ctx, obj_is_dict):
    
    def put_side_effects(o, attr, value, is_dict):
        if is_dict:
            o[attr] = value
        else:
            setattr(o, attr, value)
            
    if pre_side_effects is not None:
        if isinstance(pre_side_effects, Collection):
            pre_side_effects = list(pre_side_effects)
        else:
            raise TypeError("pre_side_effects must be a collection of Transitions")
    else:
        pre_side_effects = []

    put_side_effects(obj, 'pre_side_effects', pre_side_effects, obj_is_dict)

    if post_side_effects is not None:
        if isinstance(post_side_effects, Collection):
            post_side_effects = list(post_side_effects)
        else:
            raise TypeError("post_side_effects must be a collection of Transitions")
    else:
        post_side_effects = []

    put_side_effects(obj, 'post_side_effects', post_side_effects, obj_is_dict)

    if ctx is None:
        ctx = {}
    elif isinstance(ctx, dict):
        pass
    else:
        raise TypeError("ctx shall be dict")

    put_side_effects(obj, 'ctx', ctx, obj_is_dict)
    

def run_side_effects(side_effects, instance, context, state_current, state_next, raise_side_effect_exception):
    kwargs = {
        "instance": instance,
        "context": context,
        "state_current": state_current,
        "state_next": state_next,
    }

    errors = []
    continue_execute = True
    for se in side_effects:
        try:
            se.execute(**kwargs)
        except Exception as e:
            if se.continue_after_error:
                errors.append((se.name, e))
            else:
                if raise_side_effect_exception:
                    raise SideEffectError("Error occurred when executing side effect %s." % se.name, exc=e)
                else:
                    errors.append((se.name, e))
                    continue_execute = False
                    break

    return errors, continue_execute


class SideEffect(object):
    def __init__(self, name, ctx=None, continue_after_error=False, handler=None):
        if not isinstance(name, (str, unicode)):
            raise TypeError("name must be str.")
        self.name = name

        if isinstance(ctx, dict):
            self.ctx = ctx
        elif ctx is None:
            self.ctx = {}
        else:
            raise TypeError("ctx must be dict.")
        self.continue_after_error = continue_after_error
        self._handler = handler
    
    def execute(self, instance, context, state_current, state_next):
        context = dict(self.ctx, **context)
        self.handler(instance, context, state_current, state_next)

    def handler(self, instance, context, state_current, state_next):
        self._handler(
            instance=instance,
            context=context,
            state_current=state_current,
            state_next=state_next
        )


class SideEffectContainer(object):

    def __init__(self, pre_side_effects=None, post_side_effects=None, ctx=None):
        self.pre_side_effects = []
        self.post_side_effects = []
        self.ctx = {}
        bind_side_effects(self, pre_side_effects, post_side_effects, ctx, False)

    def _make_ctx(self, inner_ctx, context):
        return dict(dict(inner_ctx, **self.ctx), **context)
    
    def _run_side_effects(self, side_effects, instance, inner_ctx, context, state_current, state_next, raise_side_effect_exception):
        context = self._make_ctx(inner_ctx, context)
        return run_side_effects(side_effects, instance, context, state_current, state_next, raise_side_effect_exception)

    def pre_init(self, instance, inner_ctx, context, state_current, state_next, raise_side_effect_exception):
        return self._run_side_effects(
            self.pre_side_effects, instance, inner_ctx, context, state_current, state_next, raise_side_effect_exception
        )

    def post_init(self, instance, inner_ctx, context, state_current, state_next, raise_side_effect_exception):
        return self._run_side_effects(
            self.post_side_effects, instance, inner_ctx, context, state_current, state_next, raise_side_effect_exception
        )
