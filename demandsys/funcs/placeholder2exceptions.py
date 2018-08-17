# -*- coding: UTF-8 -*-
from base.exceptions import *
from django.utils.translation import ugettext_lazy as _

MAP = {
    # 获取需求
    # 获取热门需求列表
    "demand/obtain/hot/ : both user and role are null":                 # 获取热门需求时user和role全都为空
    (400, _(u"user和role字段至少有一个不能为空")),
    "demand/obtain/hot/ : page out of range":                           # 获取热门需求列表时page超出列表范围
    (400, _(u"page超出列表范围")),

    # 获取我的需求列表
    "demand/obtain/self/ : user_sid error":                             # 获取我的需求列表时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "demand/obtain/self/ : page out of range":                          # 获取我的需求列表时page超出列表范围
    (400, _(u"page超出列表范围")),

    # 获取匹配需求列表
    "demand/obtain/match/ : user_sid error":                            # 获取匹配续需求列表时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "demand/obtain/match/ : no such demand":                            # 获取匹配需求列表时发现请求中的需求不存在
    (404, _(u"找不到与请求对应的需求")),
    "demand/obtain/match/ : page out of range":                         # 获取匹配需求列表请求中的page超出列表范围
    (400, _(u"page超出列表范围")),

    # 获取指定需求
    "demand/obtain/demand/ : no such demand":                           # 获取指定需求是数据库中没有与请求中id对应的需求
    (404, _(u"没有与请求中id对应的需求")),

    # 获取需求照片数据
    "demand/obtain/photo/ : no such photo":                             # 获取需求照片时没有请求中id所对应的照片或者id和dmid不匹配
    (404, _(u"不存在这样的照片或者id和dmid不匹配")),

    # 提交需求照片
    "demand/publish/submit_photo/ : user_sid error":                    # 提交需求照片时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "demand/publish/submit_photo/ : user is not validated":             # 提交需求照片的用户还未通过审核
    (410, _(u"用户还未通过验证")),
    "demand/publish/submit_photo/ : no such demand":                    # 提交需求指定照片时指定了dmid,但是该用户没有这样的需求
    (404, _(u"指定了dmid但是该用户不存在这样的需求")),
    # FIXME 下面的错误信息会受到demandsys/funcs/issue.py/upload_photo的修改
    "demand/publish/submit_photo/ : photo error":                       # 提交需求照片时图片出现错误
    (403, _(u"图片错误")),

    # 删除需求图片
    "demand/publish/remove_photo/ : user_sid error":                    # 删除需求照片时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "demand/publish/remove_photo/ : no access":                         # 该用户没有权限删除此照片
    (403, _(u"该用户无权删除此照片")),
    "demand/publish/remove_photo/ : no such photo":                     # 删除需求照片时发现不存在与请求中id相匹配的照片
    (404, _(u"不存在与请求中id相匹配的需求照片")),

    # 发布需求
    "demand/publish/publish_demand/ : user_sid error":                  # 发布需求时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "demand/publish/publish_demand/ : user is not validated":           # 发布需求的客户还未通过审核                  #
    (410, _(u"用户还未通过验证,不能发布需求")),
    "demand/publish/publish_demand/ : quantity error":                  # 发布需求时在数量的逻辑上出现错误
    (400, _(u"最少需求量不能大于总需求量")),

    # 编辑需求
    "demand/publish/edit_demand/ : user_sid error":                     # 编辑需求时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "demand/publish/edit_demand/ : no such demand":                     # 编辑需求时找不到请求中需要编辑的需求
    (404, _(u"没有这样的需求")),
    "demand/publish/edit_demand/ : quantity error":                     # 编辑需求时最小去需求量大于总需求量
    (400, _(u"最小需求量不能大于总需求量")),

    # 关闭需求
    'demand/publish/close_demand/ : user_sid error':                    # 关闭需求时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "demand/publish/close_demand/ : no such demand":                    # 关闭需求时找不到与请求相匹配的需求
    (404, _(u"没有这样的需求")),

    # 移除需求
    'demand/publish/remove_demand/ : user_sid error':                   # 移除需求时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "demand/publish/remove_demand/ : no such demand":                   # 移除需求时找不到与请求相匹配的需求
    (404, _(u"没有这样的需求")),

}


def get_placeholder2exception(placeholder):
    if placeholder in MAP:
        return WLException(*MAP[placeholder])
    else:
        return WLException(code=500, message="%s is an undefined exception" % placeholder)


def change_error_message(placeholder, code, message):
    MAP[placeholder] = (code, message)
