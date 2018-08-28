# -*- coding: UTF-8 -*-
from apperancesys.funcs.placeholder2exceptions import MAP as APPRANCESYSMAP
from coresys.funcs.placeholder2exceptions import MAP as CORESYSMAP
from demandsys.funcs.placeholder2exceptions import MAP as DEMANDSYSMAP
from invitesys.funcs.placeholder2exceptions import MAP as INVITESYSMAP
from logsys.funcs.placeholder2exceptions import MAP as LOGSYSMAP
from ordersys.funcs.placeholder2exceptions import MAP as ORDERSYSMAP
from usersys.funcs.placeholder2exceptions import MAP as USERSYSMAP

from base.exceptions import WLException

MAP = {}
map(MAP.update, [
        APPRANCESYSMAP,
        CORESYSMAP,
        DEMANDSYSMAP,
        INVITESYSMAP,
        LOGSYSMAP,
        ORDERSYSMAP,
        USERSYSMAP,
])


def get_placeholder2exception(placeholder, error_code=None, **kwargs):
    if placeholder in MAP:
        if error_code is None:
            return WLException(code=MAP[placeholder][0], message=MAP[placeholder][1].format(**kwargs))
        else:
            return WLException(code=error_code, message=MAP[placeholder][1].format(**kwargs))
    else:
        return WLException(code=500, message="%s is an undefined exception" % placeholder)
