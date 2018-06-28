import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from ordersys.models import OrderInfo
from pushsys.choice.push_state_choice import push_state_choice
from .utils.push_receiver import push_receiver


logger = logging.getLogger(__name__)


@receiver(post_save, sender=OrderInfo)
def order_push(instance, *args, **kwargs):
    # type: (OrderInfo, list, dict) -> None
    push_receiver(
        instance,
        logger,
        push_state_choice.ORDERINFO_O_STATUS,
        'initial_o_status',
        'o_status',
        'order.orderinfo',
        {'oid': instance.id}
    )


# Conditional function for pushing when order is created.
def cond_func_order_create_push(instance, ctx):
    # type: (OrderInfo, dict) -> bool
    return instance.operator == instance.ivid.seller
