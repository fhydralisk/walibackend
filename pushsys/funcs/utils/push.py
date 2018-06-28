import hashlib
import jpush
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from pushsys.models import JPushSecret
from pushsys.exceptions import *


logger = logging.getLogger(__name__)
jpush_secret_obj = None
_jpush = None
production = False


@receiver(post_save, sender=JPushSecret)
def change_jpush_secret(instance, **kwargs):
    global jpush_secret_obj, _jpush, production
    jpush_secret_obj = instance
    _jpush = jpush.JPush(jpush_secret_obj.app_key, jpush_secret_obj.master_secret)
    production = jpush_secret_obj.production
    logger.info("JPushSecret updated.")


def get_jpush():
    # type: () -> jpush.JPush
    if _jpush is None:
        raise JPushNoAppException()

    return _jpush


def send_push_to(content, extra, all_devices=False, registration_id=None, alias=None, tags=None, raise_exception=False):
    # type: (str, bool, list, list, list, bool) -> None

    def append_audience(a_type, container, audience_list):
        if isinstance(audience_list, (list, tuple)):
            container.append(a_type(*audience_list))
        elif registration_id is not None:
            raise JPushTypeError("audience_list must be either list or tuple")
        else:
            pass

    try:
        jp = get_jpush()
        push = jp.create_push()
        push.options = {"apns_production": production, }

        if all_devices:
            push.audience = jpush.all_
        else:
            audience = []
            append_audience(jpush.registration_id, audience, registration_id)
            append_audience(jpush.alias, audience, alias)
            append_audience(jpush.tag, audience, tags)

            if len(audience) == 0:
                raise JPushValueError("No audience")

            push.audience = jpush.audience(*audience)

        push.platform = jpush.all_
        push.notification = jpush.notification(
            alert=content,
            ios=jpush.ios(alert=content, extras=extra),
            android=jpush.android(alert=content, extras=extra)
        )
        push.send()

    except Exception:
        logger.exception(
            "Exception occured when sending JPush: content=%s, reg_id=%s, alias=%s, tags=%s"
            % (str(content), str(registration_id), str(alias), str(tags))
        )
        if raise_exception:
            raise


def send_push_to_phones(content, extra, pns, raise_exception=False):

    def to_md5(pn):
        h1 = hashlib.md5()
        h1.update(pn)
        return h1.hexdigest()

    pns_md5 = map(to_md5, pns)
    send_push_to(content, extra, alias=pns_md5, raise_exception=raise_exception)
    logger.debug("Push sent to %s" % str(pns))


def initialize():
    # prevent pycharm from removing this import
    global jpush_secret_obj, _jpush, production
    jpush_secret_obj = JPushSecret.objects.last()  # type: JPushSecret
    if jpush_secret_obj is None:
        _jpush = None
        production = False
    else:
        _jpush = jpush.JPush(jpush_secret_obj.app_key, jpush_secret_obj.master_secret)
        _jpush.set_logging("DEBUG")
        production = jpush_secret_obj.production

