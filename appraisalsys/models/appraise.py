# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.conf import settings
from usersys.models import UserBase
from simplified_invite.models import InviteInfo
from appraisalsys.model_choices.appraisal_enum import a_status_choice
from demandsys.models.product import ProductWaterContent, ProductTypeL1


class ImpurityContent(models.Model):
    impcdesc = models.CharField(max_length=25, verbose_name=_("杂质描述"))
    in_use = models.BooleanField(default=True,verbose_name='是否有效')

    class Meta:
        verbose_name = '杂质'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.impcdesc


class AppraisalInfo(models.Model):
    ivid = models.OneToOneField(
        InviteInfo,
        verbose_name=_("邀请信息"),
        on_delete=models.CASCADE,
        related_name="appraisal"
    )
    a_status = models.IntegerField(_("反馈填写情况"), choices=a_status_choice.choice)
    in_accordance = models.BooleanField(_("是否符合描述"))
    final_total_price = models.FloatField(verbose_name='最终价格')
    description = models.TextField(null=True, default=None, verbose_name='具体描述')
    net_weight = models.FloatField(_("净重"), null=True)
    pure_net_weight = models.FloatField(_("结算净重"), null=True)

    wcid = models.ForeignKey(ProductWaterContent, related_name="appraisal_watercontent", verbose_name='含水量')
    impcid = models.ForeignKey(ImpurityContent, related_name="appraisal_impurity", null=True, verbose_name='杂质')

    price_1 = models.FloatField(default=None, null=True, verbose_name='报价一')
    price_2 = models.FloatField(default=None, null=True, verbose_name='报价二')
    price_3 = models.FloatField(default=None, null=True, verbose_name='报价三')

    class Meta:
        verbose_name = '评价'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.ivid.__unicode__()


class CheckPhoto(models.Model):
    uploader = models.ForeignKey(
        UserBase,
        verbose_name=_("上传人"),
        on_delete=models.CASCADE,
        related_name='appraisal_check_photo'
    )
    apprid = models.ForeignKey(
        AppraisalInfo,
        verbose_name=_("评价"),
        on_delete=models.SET_NULL,
        related_name='check_photo',
        null=True,
    )
    upload_data = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    in_use = models.BooleanField(default=True, verbose_name='是否使用')
    check_photo = models.ImageField(upload_to=settings.UPLOAD_CHECK_PHOTO, verbose_name='照片')

    class Meta:
        verbose_name = '评价照片'
        verbose_name_plural = verbose_name


class JsonSchemaOfAppraisal(models.Model):
    t1id = models.ForeignKey(
        ProductTypeL1,
        on_delete=models.CASCADE,
        related_name="json_schema_of_appraisal",
    )
    json_schema = models.TextField()
