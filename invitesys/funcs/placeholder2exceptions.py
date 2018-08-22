# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _

MAP = {
    # 邀请获取
    # 获取我的邀请
    "invite/obtain/self/ : user_sid error":                     # 获取我的邀请列表时user_sid不存在或者已经过期
    (404, _(u"未找到user_sid")),
    "invite/obtain/self/ : page out of range":                  # 获取我的邀请列表时怕个超出列表范围
    (400, _(u"page超出列表范围")),

    # 获取邀请详情
    "invite/obtain/detail/ : user_sid error":                   # 获取邀请详情时user_sid不存在或者已经过期
    (404, _(u"未找到user_sid")),
    "invite/obtain/detail/ : no such invite":                   # 获取邀请详情时找不到与请求匹配的邀请
    (404, _(u"没有这样的邀请信息")),
    "invite/obtain/detail/ ; no access":                        # 获取邀请详情时该邀请不属于当前用户
    (401, _(u"该邀请不属于当前用户")),

    # 发布邀请
    "invite/launch/launch/ : user_sid error":                   # 发起邀请时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "invite/launch/launch/ : user is not validated":            # 发起邀请时用户还没有通过审核
    (410, _(u"该用户还未通过审核")),
    "invite/launch/launch/ : invalid photo id":                 # 发起邀请时庆祝中有的photo id是无效的
    (400, _(u"请求中存在无效的photo id")),
    "invite/launch/launch/ : no such demand - not in use":      # 发起邀请时所邀请的需求不在使用中
    (404, _(u"该需求不在使用当中")),
    "invite/launch/launch/ : no such demand - expire":          # 发起邀请时邀请对象已经到期
    (404, _(u"邀请对象已经到期")),
    "invite/launch/launch/ : no such demand - role doesn't match":  # 发起邀请时邀请对象和发起邀请的用户role一致
    (404, _(u"邀请对象和发起邀请的用户role一致")),
    "invite/launch.launch/ : min quantity not satisfied":       # 发起邀请时并不满足最低需求量
    (403, _(u"不能满足最低需求")),
    "invite/launch/launch/ : exceed max quantity":              # 发起邀请时超出最大需求量
    (403, _(u"超出最大需求量")),

    # 邀请流程
    "invite/flow/handle/ : user_sid error":                     # 操做邀请流程时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "invite/flow/handle/ : action error":                       # 操作邀请流程时操作错误
    (403, _(u"操作错误")),
    "invite/flow/handle/ : no such invite":                     # 操作邀请流程时没有找到与请求匹配的invite
    (404, _(u"没有这样的邀请流程")),

    # 订单照片
    # 提交邀请照片
    "invite/photo/upload/ : user_sid":                          # 提交邀请照片时user_sid已过期或者不存在
    (404, _(u"未找到user_sid")),
    "invite/photo/upload/ : no such invite":                    # 提交照片时没有与请求中ivid相匹配的invite
    (404, _(u"没有这样的invite")),
    "invite/photo/upload/ : only seller":                       # 只有卖家能够提交照片
    (403, _("only seller can upload")),
    # FIXME 以下错误信息会在invitesys/funcs/invites.py/upload-invite_photo中被修改
    "invite/photo/upload/ : photo error":                       # 提交照片时图片出现某些错误
    (400, _(u"图片错误")),

    # 删除邀请照片
    "invite/photo/delete/ : user_sid error":                    # 删除邀请照片时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "invite/photo/delete/ : no such photo":                     # 删除邀请照片时没有与请求中photo_id匹配的照片
    (404, _(u"不存在这样的照片")),
    "invite/photo/delete/ : is not uploader":                   # 删除照片的用胡并不所以上传者
    (404, _(u"这张照片不是该用户上传的")),
    "invite/photo/delete/ : is not seller":                     # 该照片所在订单的卖家不是该用户
    (404, _(u"该照片所在订单的卖家不是该用户")),
    # FIXME 以下错误信息会在invitesys/funcs/invites.py/delete-invite_photo中被修改
    "invite/photo/delete/ : status error":                      # 不能删除出于该状态下的照片
    (403, _(u"不能删除处于该状态下的照片")),

    # 获取邀请照片信息
    "invite/photo/obtain/ : user_sid_error":                    # 获取邀请照片信息时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "invite/photo/obtain/ : no such photo":                     # 获取照片信息是没有与请求中photo_id相匹配的照片
    (404, _(u"没有这样的照片")),
    "invite/photo/obtain/ : no access":                         # 该用户不是该照片所在邀请的卖家或者买家
    (404, _(u"该用户不是这张照片所在邀请的卖家或者买家")),
    "invite/photo/obtain/ : is not uploader":                   # 该照片不属于任何邀请,但该用户不是这张照片的上传者
    (404, _(u"该照片不属于任何邀请,但是该用户不是它的上传者")),

    # 合同获取
    "invite/contract/ : no such contract in function get_contract_obj":    # 不存在这样的合同
    (404, _(u"没有这样的合同")),
    # 获取合同信息
    "invite/contract/info/ : user_sid error":                   # 获取合同信息时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),

    # 获取合同内容
    "invite/contract/content/ : user_sid error":                # 获取合同内容时user_sid已过期或不存在
    (404, _(u"未找到user_sid")),

    # 合同签署或者拒绝
    "invite/contract/sign/ : user_sid error":                   # 签署合同时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "invite/contract/sign/ : cannot change sign status":        # 不能改变合同状态
    (403, _(u"不能改变合同的状态")),
    "invite/contract/sign/ : already signed or rejected":       # 合同已经签署或拒绝
    (403, _(u"合同已经签署或者拒绝"))
}
