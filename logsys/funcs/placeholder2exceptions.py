# -*- coding: UTF-8 -*-
from base.exceptions import *
from django.utils.translation import ugettext_lazy as _

MAP = {
    # 获取订单日志
    "log/order/obtain_order/ : user_sid error":                 # 获取日志时user_sid不存在或已过期
    (404, _(u"未找到user_sid")),
    "log/order/obtain_order/ : no such order":                  # 获取日志时没有相应的订单
    (404, _(u"不存在这样的订单")),

    "log/order/obtain_protocol/ : user_sid error":              # 获取订单协议日志时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "log/order/obtain_protocol/ : no such order":               # 获取订单协议日志时没有相应的订单
    (404, _(u"不存在这样的订单")),
}


def get_placeholder2exception(placeholder):
    if placeholder in MAP:
        return WLException(*MAP[placeholder])
    else:
        return WLException(code=500, message="%s is an undefined exception" % placeholder)


def change_error_message(placeholder, code, message):
    MAP[placeholder] = (code, message)
