import hashlib
import jpush
from django.db.models.signals import post_save
from django.dispatch import receiver
from pushsys.models import JPushSecret, PushTemplate
from pushsys.exceptions import *


jpush_secret_obj = JPushSecret.objects.last()  # type: JPushSecret
if jpush_secret_obj is None:
    _jpush = None
else:
    _jpush = jpush.JPush(jpush_secret_obj.app_key, jpush_secret_obj.master_secret)
    _jpush.set_logging("DEBUG")


@receiver(post_save, sender=JPushSecret)
def change_jpush_secret(instance, **kwargs):
    global jpush_secret_obj, _jpush
    jpush_secret_obj = instance
    _jpush = jpush.JPush(jpush_secret_obj.app_key, jpush_secret_obj.master_secret)


def get_jpush():
    if _jpush is None:
        raise JPushNoAppException

    return _jpush


def send_push_to(content, registration_id=None, alias=None, tags=None, raise_exception=False):
    # type: (str, list, list, list) -> None

    def append_audience(a_type, container, audience_list):
        if isinstance(audience_list, (list, tuple)):
            container.append(a_type(*audience_list))
        elif registration_id is not None:
            raise JPushTypeError("audience_list must be either list or tuple")
        else:
            pass

    try:
        jp = get_jpush()

        audience = []
        append_audience(jpush.registration_id, audience, registration_id)
        append_audience(jpush.alias, audience, alias)
        append_audience(jpush.tag, audience, tags)

        if len(audience) == 0:
            raise JPushValueError("No audience")

        push = jp.create_push()

        push.audience = jpush.audience(*audience)
        push.platform = jpush.all_
        push.notification = jpush.notification(alert=content)
        push.send()

    except Exception as e:
        if raise_exception:
            raise
        else:
            # TODO: How to log this?

            pass


def send_push_to_phones(content, pns, raise_exception):

    def to_md5(pn):
        h1 = hashlib.md5()
        h1.update(pn)
        return h1.hexdigest()

    pns_md5 = map(to_md5, pns)
    send_push_to(content, alias=pns_md5, raise_exception=raise_exception)
