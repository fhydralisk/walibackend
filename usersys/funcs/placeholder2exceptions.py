# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _

MAP = {
    # 注册过程，分别是提交手机号，提交验证码和设置登录密码
    "user/register/pn/pn/ : format of phone number is incorrect":     # 注册时提交错误的手机号
    (401, _(u"不存在这样的手机号")),

    "user/register/pn/validate/ :  Validation error":                 # 提交验证码时填入错误的验证码
    (401, _(u"验证码错误")),
    "user/register/pn/validate/ : sid error":                         # 提交验证码时sid不存在或者已经过期
    (404, _(u"未找到sid，sid可能已过期")),
    "user/register/pn/validate/ : sid conflicts with pn":             # 提交验证码时pn和sid不匹配
    (409, _(u"pn和sid不匹配")),
    "user/register/pn/validate/ : unexpected fork":                   # 提交验证码时出现未知错误
    (500, _(u"未知错误")),

    "user/register/pn/password/ : sid error":                         # 设置密码时sid不存在或者已经过期
    (404, _(u"未找到sid，sid可能已经过期")),
    "user/register/pn/password/ : sid conflicts with pn":             # 设置密码时sid和pn不匹配
    (409, _(u"pn和sid不匹配")),
    "user/register/pn/password/ : user exists":                       # 设置密码时该用户已经存在
    (401, _(u"该手机号已经注册过用户")),
    "user/register/pn/password/ : not validated":                     # 设置密码时发现该手机号还没有通过验证
    (405, _(u"该手机号还没有经过验证码验证")),

    # 登录和注销登录过程
    "user/login/login/ : authenticate failed":                        # 登录失败，原因可能是密码错误，也可能是选择的role错误
    (401, _(u"登录失败")),

    "user/login/logout/ : sid error":                                 # 注销登录时找不到sid
    (404, _(u"未找到sid")),
    "user/login/logout/ : pn conflicts with sid":                     # 注销登录时sid和pn不匹配
    (409, _(u"pn和sid不匹配")),

    # 获取当前用户信息
    "user/info/self/ : user_sid not in url":                          # 获取当前用户信息的get请求的参数中没有user_sid
    (400, _(u"bad request")),
    "user/info/self/ : user_sid not exist":                           # 获取当前用户信息的get请求中user_sid不存在
    (404, _(u"user_sid不存在")),

    # 找回密码，
    # 提交手机号,和注册时提交手机号调用的函数一模一样,关系映射也自然和那里一模一样。
    # 提交验证码,和注册时提交验证码调用的函数一模一样,关系映射也一模一样。
    # 提交新密码
    "user/resetpasswd/pn/validate/ : sid error":                      # 提交新密码时找不到sid或者sid已经过期
    (404, _(u"未找到sid,或者该手机号还未注册")),
    "user/resetpasswd/pn/validate/ : pn conflicts with sid":          # 提交新密码是sid和pn不匹配
    (409, _(u"pn和sidd不匹配")),
    "user/resetpasswd/pn/validate/ : format of password not valid":   # 提交新密码时新密码格式不正确
    (403, _(u"密码格式错误")),
    "user/resetpasswd/pn/validate/ : not validated":                  # 该手机号还未经过验证
    (405, _(u"该手机号还没有经过验证码验证")),

    # 修改密码
    "user/resetpasswd/changepasswd/ : Authenticate failed":            # 修改密码时原密码验证错误
    (403, _(u"密码验证错误")),
    "user/resetpasswd/changepasswd/ : user_sid error":                 # 修改密码时user_sid不存在或者已经过期
    (404, _(u"未找到user_sid")),

    # 获取已提交的营业执照,身份证的图片
    "user/validate/fetch_photo/ : user_sid error":                     # 获取已提交的营业执照或身份证图片时时user_sid不存在或者已经过期
    (401, _(u"未找到user_sid")),
    "user/validate/fetch_photo/ : no such photo":                      # 想要获取提交的营业执照或身份证图片时发现用户还没有提交该照片
    (404, _(u"未上传该照片")),

    # 提交营业执照或者身份证图片
    "user/validate/submit_photo/ : bad request":                       # 提交营业执照或者身份证图片的请求有误
    (400, _(u"请求有误")),
    "user/validate/submit_photo/ : user_sid error":                    # 提交营业执照或者身份证图片时user_sid不正确或者已经过期
    (404, _(u"未找到user_sid")),
    "user/validate/submit_photo/ : validation submitted":              # 已经提交了审核,无法更改
    (401, _(u"已经提交过审核,不能更改图片")),
    # FIXME 此处的错误信息会被funcs/validate.py/submit_validate_photo修改,若想修改请到funcs/validate.py文件删掉相应代码
    "user/validate/submit_photo/ : photo error":                       # 提交图片时图片有误,错误信息由submit_validate_photo函数提供
    (403, _(u"图片错误")),

    # 删除营业执照或者身份证图片
    "user/validate/delete_photo/ : user_sid error":                    # 删除营业执照或者身份证的图片时user_sid不存在或者已经过期
    (404, _(u"未找到user_sid")),
    "user/validate/delete_photo/ : validation submitted":              # 已经提交了审核,无法更改
    (401, _(u"已经提交过审核,不能修改")),

    # 保存其他信息与提交审核
    "user/validate/submit_info/ : user_sid error":                     # 想要保存或者提交审核时user_sid不存在或者已过期
    (404, _(u"未找到user_sid")),
    "user/validate/submit_info/ : validation submitted":               # 已经提交了审核,无法更改
    (401, _(u"已经提交过审核,不能修改信息")),
    # FIXME 这里具体的code和message会由funcs/validate.py/save_validate给出
    "user/validate/submit_info/ : information is incomplete":          # 想要提交审核时各信息填的不完整
    (403, _(u"信息不完整")),

    # 获取用户认证信息
    "user/validate/fetch_info/ : user_sid error":                      # 获取用户认证信息时user_sid不存在或者已经过期
    (404, _(u"未找到user_sid")),
    "user/validate/fetch_info/ : bad request":                         # 获取用户认证信息时请求格式出错
    (400, _(u"请求格式错误"))
}

