# -*- coding: UTF-8 -*-
from base.exceptions import *
from django.utils.translation import ugettext_lazy as _

MAP = {
    "appearance/banner/ : no banner in  get_banner_etag":
    (404, _(u"no banner")),
    "appearance/banner/ : no banner in get_banner":
    (404, _("no banner")),
}
