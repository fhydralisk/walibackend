import logging
import operator
from django.utils.module_loading import import_string
from .template import get_state_change_template
from .push import send_push_to_phones
from pushsys.exceptions import *


def push_receiver(instance, logger, template_state_name,
                  initial_status_attr, status_attr, extra_type, extra_content):
    # type: (object, logging.Logger, str, str, str, str, object) -> None
    try:
        initial_status = getattr(instance, initial_status_attr)
        status = getattr(instance, status_attr)
    except AttributeError:
        logger.exception("AttributeError")
        return

    logger.debug("%s change detected, from %s to %s. getting templates."
                 % (template_state_name, str(initial_status), str(status)))

    template, ctx = get_state_change_template(
       template_state_name, initial_status, status
    )

    if template is None:
        return

    logger.debug("Template: %s" % template.__unicode__())

    if ctx is None:
        logger.warning("Trying to make a %s push without push_ctx field in the template row."
                       "initial=%s, target=%s" % (template_state_name, str(initial_status), str(status)))
        return

    # Conditional Push. checks ctx["condition_func"]
    if "condition_func" in ctx:
        cond_func_str = ctx["condition_func"]
        try:
            condition_func = import_string(cond_func_str)
            if not condition_func(instance, ctx):
                logger.debug("Do not send push %s %s->%s, because it does not meets the condition."
                             % (template_state_name, str(initial_status), str(status)))
                return
        except ImportError:
            logger.exception("Trying to call condition_func of %s %s->%s. but cannot import this function %s."
                             % (template_state_name, str(initial_status), str(status), cond_func_str))
            return
        except TypeError:
            logger.exception("Trying to call condition_func of %s %s->%s. but cannot call this function %s."
                             % (template_state_name, str(initial_status), str(status), cond_func_str))
            return

    try:
        # receivers: [ '13800138000', '15505505555', ... ]
        receivers = [operator.attrgetter("%s.pn" % x)(instance) for x in ctx['receivers']]
        # TODO: Move this into celery
        try:
            send_push_to_phones(
                template.template,
                {"type": extra_type, "content": extra_content},
                receivers,
                False
            )
        except JPushNoAppException:
            logger.error("JPush cannot start because master key and app label do not exist in database.")

    except KeyError:
        logger.error("%s push_ctx does not have receivers key."
                     "initial=%s, target=%s" % (template_state_name, str(initial_status), str(status)))
    except AttributeError:
        logger.error("%s push_ctx's receiver field is not valid. order info object don't have that attributes"
                     "initial=%s, target=%s" % (template_state_name, str(initial_status), str(status)))
