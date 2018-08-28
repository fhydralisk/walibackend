# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _

MAP = {
    # 订单获取
    # 获取我的订单
    "order/info/list/ : user_sid error":                         # 获取我的订单时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "order/info/list/ : order_type error":                       # 获取我的订单时订单类型无效
    (400, _(u"无效的订单类型")),
    "order/info/list/ : page out of range":                      # 获取我的订单时page超出列表范围
    (400, _(u"page超出列表范围")),

    # 获取指定订单和票据信息
    "order/info/order/ : user_sid error":                        # 获取指定订单时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "order/info/order/ : no such order":                         # 获取指定订单时不存在与请求中oid相匹配的订单
    (404, _(u"不存在这样的订单")),

    # 订单操作
    # 非付款订单流程
    "order/operate/order/ : user_sid_error":                     # 操作订单时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "order/operate/order/ : invalid action of buyer":            # 这不是一个有效的买家操作
    (403, _(u"这不是一个有效的买家操作")),
    "order/operate/order/ : invalid action of seller":           # 这不是一个有效的卖家操作
    (403, _(u"这不是一个有效的卖家操作")),
    "order/operate/order/ : invalid user":                       # 这不是一个有效的用户
    (403, _(u"这不是一个有效的用户")),
    "order/operate/order/ : no such oid":                        # 操作订单时不存在和请求中oid匹配的订单
    (404, _(u"不存在这样的订单")),

    # 协议执行流程
    "order/operate/photocol/ : user_sid error":                  # 操作流程时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "order/operate/photocol/ : invalid action of buyer":         # 这不是一个有效的买家操作
    (403, _(u"这不是一个有效的买家操作")),
    "order/operate/photocol/ : invalid action of seller":        # 这不是一个有效的卖家操作
    (403, _(u"这不是一个有效的卖家操作")),
    "order/operate/photocol/ : invalid user":                    # 这不是一个有效的用户
    (403, _(u"这不是一个有效的用户")),
    "order/operate/photocol/ : no such oid":                     # 操作流程时不存在和请求中oid匹配的订单
    (404, _(u"不存在这样的订单")),

    # 提交订单照片
    "order/photo/upload/ : user_sid error":                      # 上传照片时user_sod不存在或者已过期
    (404, _(u"未找到user_sid")),
    "order/photo/upload/ : no such oid":                         # 上传照片时不存在和请求中oid匹配的订单
    (404, _(u'不存在这样的订单')),
    "order/photo/upload/ : cannot submit this photo":            # 照片类型不对,不能上传
    (403, _(u"不能上传此照片")),
    "order/photo/upload/ : user role does not match":            # 用户类型不对
    (403, _(u"该用户类类型不能上传此照片")),
    "order/photo/upload/ : photo error":                         # 上传的图片出现某些问题
    (400, '{error_message}'),

    # 删除订单照片
    "order/photo/delete/ : user_sid error":                      # 删除照片时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "order/photo/delete/ : cannot remove":                       # 不能移除这张照片
    (403, _(u"不能移除张照片")),
    "order/photo/delete/ : user role error":                     # 该用户角色不能删除这张照片
    (403, _(u"该用户角色不能删除这张照片")),

    # 获取订单照片数据
    "order/photo/obtain/ : user_sid_error":                      # 获取照片时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "order/photo/obtain/ : no such photo":                       # 获取或者删除照片时没有和请求中photo_id相匹配的照片
    (404, _(u"该照片不存在")),
}

