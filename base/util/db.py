"""
Database utilities
"""
import logging
from django.db.models import Model, QuerySet
from django.db.models.signals import post_save, post_delete


default_logger = logging.getLogger(__name__)


def update_instance_from_dict(instance, dic, save=False):
    for k, v in dic.items():
        if hasattr(instance, k):
            if isinstance(v, dict):
                update_instance_from_dict(getattr(instance, k), v, save)
            else:
                setattr(instance, k, v)

    if save:
        instance.save()


class LastLineConfigManager(object):

    CLZ_MODEL = None
    _instance = None
    cls_logger = None

    def __init__(self, reload_callback=None, logger=None):
        if not issubclass(self.CLZ_MODEL, Model):
            raise TypeError
        if callable(reload_callback):
            self.reload_callback = reload_callback
        elif reload_callback is not None:
            raise TypeError("reload callback must be None or callable")
        else:
            self.reload_callback = None

        if isinstance(logger, logging.Logger):
            self.cls_logger = logger
        elif logger is None:
            if self.cls_logger is None:
                self.cls_logger = default_logger
            else:
                if not isinstance(self.cls_logger, logging.Logger):
                    raise TypeError("logger must be a Logger class.")
        else:
            raise TypeError("logger must be a Logger class.")

        post_save.connect(self.reload, sender=self.CLZ_MODEL)
        post_delete.connect(self.reload, sender=self.CLZ_MODEL)

    def reload(self, **kwargs):
        self.cls_logger.info("%s is reloading due to signals" % self.CLZ_MODEL.__name__)
        self.do_load()
        if self.reload_callback is not None:
            self.reload_callback(self._instance)

    def do_load(self):
        try:
            self._instance = self.extra_filter(self.CLZ_MODEL.objects).last()
        except NotImplementedError:
            self._instance = self.CLZ_MODEL.objects.last()

    @staticmethod
    def extra_filter(qs):
        # type: (QuerySet) -> QuerySet
        raise NotImplementedError

    @property
    def instance(self):
        if self._instance is None:
            self.do_load()

        return self._instance
