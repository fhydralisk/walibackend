import operator
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from invitesys.models import InviteInfo
from .utils.template import get_system_template
from .utils.push import send_push_to_phones
from pushsys.choice.push_state_choice import push_state_choice
from pushsys.exceptions import JPushNoAppException


logger = logging.getLogger(__name__)


@receiver(post_save, sender=InviteInfo)
def order_push(instance, *args, **kwargs):
    # type: (InviteInfo, list, dict) -> None
    template, ctx = get_system_template(
        push_state_choice.INVITEINFO_I_STATUS, instance.initial_i_status, instance.i_status
    )

    if template is None:
        return

    if ctx is None:
        logger.warning("Trying to make a invite push without push_ctx field in the template row."
                       "initial=%s, target=%s" % (str(instance.initial_i_status), str(instance.i_status)))
        return

    try:
        receivers = [operator.attrgetter("%s.pn" % x)(instance) for x in ctx['receivers']]
        # TODO: Move this into celery
        try:
            send_push_to_phones(template.template, receivers, False)
        except JPushNoAppException:
            logger.error("JPush cannot start because master key and app label do not exist in database.")

    except KeyError:
        logger.error("invite push_ctx does not have receivers key."
                     "initial=%s, target=%s" % (str(instance.initial_i_status), str(instance.i_status)))
    except AttributeError:
        logger.error("invite push_ctx's receiver field is not valid. order info object don't have that attributes"
                     "initial=%s, target=%s" % (str(instance.initial_i_status), str(instance.i_status)))
