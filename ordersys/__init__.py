# coding=utf-8
from django.apps import AppConfig
import os

default_app_config = 'ordersys.UserConfig'

VERBOSE_APP_NAME = u"订单"


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class UserConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME