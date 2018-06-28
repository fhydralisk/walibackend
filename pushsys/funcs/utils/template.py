import json
from pushsys.models import PushTemplate

# TODO: Hook the PushTemplate's post_save. update cache.


def get_state_change_template(state_name, state_from, state_after):
    # TODO: Cache Here.
    state_templates = PushTemplate.objects.filter(in_use=True, push_state_name=state_name)
    for template in state_templates:
        if template.push_ctx is None:
            continue
        try:
            ctx = json.loads(template.push_ctx)
            # If both state_from and state_after not in ctx dictionary, then the ctx is invalid for this function.
            if "state_from" not in ctx and "state_after" not in ctx:
                raise KeyError

            # If both or one of (state_from, state_after) in ctx, check if it is matched.
            if ctx.get("state_from", state_from) == state_from and ctx.get("state_after", state_after) == state_after:
                return template, ctx
        except (KeyError, ValueError):
            continue

    return None, None


def render_template(template, **kwargs):
    pass
