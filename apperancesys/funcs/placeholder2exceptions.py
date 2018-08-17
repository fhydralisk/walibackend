# -*- coding: UTF-8 -*-
from base.exceptions import *
from django.utils.translation import ugettext_lazy as _

MAP = {
    "appearance/banner/ : no banner in  get_banner_etag":
    (404, _(u"no banner")),
    "appearance/banner/ : no banner in get_banner":
    (404, _("no banner")),
}


def get_placeholder2exception(placeholder):
    if placeholder in MAP:
        return WLException(*MAP[placeholder])
    else:
        return WLException(code=500, message="%s is an undefined exception" % placeholder)


def change_error_message(placeholder, code, message):
    MAP[placeholder] = (code, message)
