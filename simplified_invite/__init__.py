# coding=utf-8
from django.apps import AppConfig
import os

default_app_config = 'simplified_invite.simplified_inviteConfig'

VERBOSE_APP_NAME = u"邀请"


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class simplified_inviteConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME