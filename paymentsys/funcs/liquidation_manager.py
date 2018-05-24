"""

"""
from django.utils.module_loading import import_string
from django.conf import settings


class AbstractLiquidationCallback(object):

    def confirm_liquidation(self, order, context):
        raise NotImplementedError


class AbstractLiquidationManager(object):

    def generate(self, order, amount):
        raise NotImplementedError

    def respond_liquidation(self, liquidation, response):
        raise NotImplementedError

    def get_callback(self):
        str_callback_class = settings.PAYMENT["LIQUIDATION_MANAGER"]["CALLBACK"]
        callback = import_string(str_callback_class)  # type: AbstractLiquidationCallback
        return callback


class DummyLiquidationManager(AbstractLiquidationManager):
    def generate(self, order, amount):
        self.respond_liquidation(None, {"order": order})

    def respond_liquidation(self, liquidation, response):
        self.get_callback().confirm_liquidation(response["order"], None)


manager = import_string(settings.PAYMENT["LIQUIDATION_MANAGER"]["CLASS"])(
    **settings.PAYMENT["LIQUIDATION_MANAGER"].get("ARGS", {})
)  # type: AbstractLiquidationManager
