from django.db.models.signals import post_save
from django.dispatch import receiver
from ordersys.models import OrderInfo, OrderProtocol
from logsys.models import LogOrderStatus, LogOrderProtocolStatus
from base.exceptions import WLException, default_exception, Error500, Error404
from usersys.funcs.utils.usersid import user_from_sid
from usersys.models import UserBase


@receiver(post_save, sender=OrderInfo)
def log_order_change(instance, **kwargs):
    # type: (OrderInfo, dict) -> None
    operator = getattr(instance, 'operator', None)
    log_entry = LogOrderStatus(oid=instance, operator=operator, o_status=instance.o_status)
    log_entry.save()


@receiver(post_save, sender=OrderProtocol)
def log_protocol_change(instance, **kwargs):
    # type: (OrderProtocol, dict) -> None
    operator = getattr(instance, 'operator', None)
    log_entry = LogOrderProtocolStatus(
        opid=instance,
        operator=operator,
        p_status=instance.p_status,
        p_operate_status=instance.p_operate_status
    )
    log_entry.save()


@default_exception(Error500)
@user_from_sid(Error404)
def obtain_order_log(user, oid):
    # type: (UserBase, OrderInfo) -> QuerySet
    invite = oid.ivid
    if invite.uid_s != user and invite.uid_t != user:
        raise WLException(404, "No such order")

    return LogOrderStatus.objects.filter(oid=oid)


@default_exception(Error500)
@user_from_sid(Error404)
def obtain_order_protocol_log(user, opid):
    # type: (UserBase, OrderProtocol) -> QuerySet
    invite = opid.oid.ivid
    if invite.uid_s != user and invite.uid_t != user:
        raise WLException(404, "No such order")

    return LogOrderProtocolStatus.objects.filter(opid=opid)
