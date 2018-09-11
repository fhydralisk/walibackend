import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from simplified_invite.models import InviteInfo
from pushsys.choice.push_state_choice import push_state_choice
from .utils.push_receiver import push_receiver


logger = logging.getLogger(__name__)


@receiver(post_save, sender=InviteInfo)
def invite_push(instance, *args, **kwargs):
    # type: (InviteInfo, list, dict) -> None
    push_receiver(
        instance,
        logger,
        push_state_choice.SIMPLIFIED_INVITEINFO_I_STATUS,
        'initial_i_status',
        'i_status',
        'simplified_invite.inviteinfo',
        {'ivid': instance.id}
    )
