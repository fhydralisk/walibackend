import logging
import jpush
from pushsys.funcs.pusher import AbstractPusher
from pushsys.models import JPushSecret
from .jp_secret_manager import JPSecretManager
from .exceptions import *


logger = logging.getLogger(__name__)


class JPusher(AbstractPusher):

    def __init__(self):
        self._jpush = None
        self._production = False
        self.jp_secret_manager = JPSecretManager(self._reload_jp, logger)

    def _reload_jp(self, instance):
        # type: (JPushSecret) -> None
        if instance is not None:
            self._jpush = jpush.JPush(instance.app_key, instance.master_secret)
            self._production = instance.production
        else:
            self._jpush = None
            self._production = False

    @property
    def jp(self):
        if self._jpush is None and self.jp_secret_manager.instance is not None:
            self._reload_jp(self.jp_secret_manager.instance)

        return self._jpush

    def send_push_to(self, content, extra, all_devices=False, registration_id=None, alias=None, tags=None,
                     raise_exception=False):
        # type: (str, bool, list, list, list, bool) -> None

        def append_audience(a_type, container, audience_list):
            if isinstance(audience_list, (list, tuple)):
                container.append(a_type(*audience_list))
            elif registration_id is not None:
                raise JPushTypeError("audience_list must be either list or tuple")
            else:
                pass

        try:
            jp = self.jp
            if jp is None:
                logger.warning("Cannot send JPush message due to failure on loading jpush client."
                               "Please check the correctness of master key of JPush.")
                return

            push = jp.create_push()
            push.options = {"apns_production": self._production, }

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
