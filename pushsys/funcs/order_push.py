import operator
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from ordersys.models import OrderInfo
from .utils.template import get_state_change_template
from .utils.push import send_push_to_phones
from pushsys.choice.push_state_choice import push_state_choice


logger = logging.getLogger(__name__)


@receiver(post_save, sender=OrderInfo)
def order_push(instance, *args, **kwargs):
    # type: (OrderInfo, list, dict) -> None
    logger.debug("OrderInfo change detected, from %s to %s. getting templates."
                 % (str(instance.initial_o_status), str(instance.o_status)))

    template, ctx = get_state_change_template(
        push_state_choice.ORDERINFO_O_STATUS, instance.initial_o_status, instance.o_status
    )

    if template is None:
        return

    logger.debug("Template: %s" % template.__unicode__())

    if ctx is None:
        logger.warning("Trying to make a order push without push_ctx field in the template row."
                       "initial=%s, target=%s" % (str(instance.initial_o_status), str(instance.o_status)))
        return

    try:
        receivers = [operator.attrgetter("%s.pn" % x)(instance) for x in ctx['receivers']]
        # TODO: Move this into celery
        send_push_to_phones(template.template, receivers, False)
    except KeyError:
        logger.error("order push_ctx does not have receivers key."
                     "initial=%s, target=%s" % (str(instance.initial_o_status), str(instance.o_status)))
    except AttributeError:
        logger.error("order push_ctx's receiver field is not valid. order info object don't have that attributes"
                     "initial=%s, target=%s" % (str(instance.initial_o_status), str(instance.o_status)))
