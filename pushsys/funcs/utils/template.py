import json
import logging
from pushsys.models import PushTemplate
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# TODO: This shall be move into memcached.
logger = logging.getLogger(__name__)
cached_state_templates_dict = None


def reload_templates():
    global cached_state_templates_dict
    state_templates = PushTemplate.objects.filter(in_use=True)
    cached_state_templates_dict = {}
    for template in state_templates:
        if template.push_state_name:
            former = cached_state_templates_dict.get(template.push_state_name, [])
            former.append(template)
            cached_state_templates_dict[template.push_state_name] = former

    logger.info("Push Template reloaded into cache.")


# Hook the PushTemplate's post_save. update cache.
@receiver(signal=[post_save, post_delete], sender=PushTemplate)
def update_templates(**kwargs):
    reload_templates()


def get_state_change_template(state_name, state_from, state_after):
    # Try accessing cached dict first
    # state_templates = PushTemplate.objects.filter(in_use=True, push_state_name=state_name)
    if cached_state_templates_dict is None:
        reload_templates()

    state_templates = cached_state_templates_dict[state_name]

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
