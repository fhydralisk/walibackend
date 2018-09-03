# coding=utf-8
from .admin_site import admin_site
from model_admin import core_admin, order_admin, user_admin, demand_admin, invite_admin, log_admin, push_admin, \
    payment_admin
from django.contrib import admin

managed = [
    core_admin,
    order_admin,
    user_admin,
    demand_admin,
    invite_admin,
    log_admin,
    push_admin,
    payment_admin,
]

admin.site.site_header = '瓦力环保科技后台管理系统'
admin.site.site_title = '瓦力环保科技后台管理系统'


def register_all():
    for m in managed:
        if hasattr(m, 'to_register'):
            # raise ZeroDivisionError
            for r in m.to_register:
                admin_site.register(*r)
                # raise Exception(*r)


register_all()
