# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _

MAP = {
    # 获取地址信息
    # 获取市级地址
    "core/address/city/ : expect pid":            # 获取市级地址的请求中没有省级地址的id
    (400, _(u"请求中缺少pid字段")),
    "core/address/city/ : pid not exist":         # 获取市级地址时没有与请求中pid相匹配的省
    (404, _(u"未找到与pid相匹配的省")),

    # 获取区级地址
    "core/address/area/ : expect cid":            # 获取区级地址时庆祝中没有市级地址的id
    (400, _(u"请求中缺少cid字段")),
    "core/address/area/ : cit not exist":         # 获取区级地址时没有与请求中cid相匹配的市
    (404, _(u"未找到与cid相匹配的市")),
}
