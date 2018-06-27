import json
from pushsys.models import PushTemplate


def get_system_template(state_name, state_from, state_after):
    # TODO: Cache Here.
    state_templates = PushTemplate.objects.filter(in_use=True, push_state_name=state_name)
    for template in state_templates:
        if template.push_ctx is None:
            continue
        try:
            ctx = json.loads(template.push_ctx)
            if ctx["state_from"] == state_from and ctx["state_after"] == state_after:
                return template, ctx
        except (KeyError, ValueError):
            continue

    return None, None


def render_template(template, **kwargs):
    pass
