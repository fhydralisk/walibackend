# coding=utf-8
from django.contrib.admin.sites import AdminSite


class WaliBgSite(AdminSite):
    site_header = "瓦力环保科技后台管理系统"
    site_title = "瓦力环保科技后台管理系统"


admin_site = WaliBgSite(name="backgroundsys")
