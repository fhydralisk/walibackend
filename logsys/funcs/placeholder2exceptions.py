# -*- coding: UTF-8 -*-
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

