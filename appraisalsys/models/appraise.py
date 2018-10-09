# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.conf import settings
from usersys.models import UserBase
from simplified_invite.models import InviteInfo
from appraisalsys.model_choices.appraisal_enum import a_status_choice, template_choice
from demandsys.models.product import ProductTypeL1
from simple_history.models import HistoricalRecords
from appraisalsys.model_choices.appraisal_enum import change_reason_choice


class ImpurityContent(models.Model):
    impcdesc = models.CharField(max_length=255, verbose_name=_("Impurity Content"))
    in_use = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('杂质')
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.impcdesc


class AppraisalInfo(models.Model):

    ivid = models.OneToOneField(
        InviteInfo,
        verbose_name=_("邀请信息"),
        on_delete=models.CASCADE,
        related_name="appraisal",
    )
    a_status = models.IntegerField(_("反馈填写情况"), choices=a_status_choice.choice)
    in_accordance = models.BooleanField(_("是否符合描述"))

    final_total_price = models.FloatField(verbose_name='最终价格', null=True)
    final_price = models.FloatField(_("单价"))
    net_weight = models.FloatField(_("净重"))
    pure_net_weight = models.FloatField(_("结算净重"), null=True)
    water_content = models.FloatField(_('含水量'), null=True)
    impurity_content = models.FloatField(_('杂质含量'), null=True)
    tare = models.FloatField(_("扣重"), null=True)
    deduction_ratio = models.FloatField(_("扣杂比率"), null=True)

    parameter = models.TextField(null=True, verbose_name=_('其余参数'))

    history = HistoricalRecords()
    change_reason = models.IntegerField(
        verbose_name=_('修改原因'),
        default=change_reason_choice.BUYER_SUBMIT,
        max_length=100,
        choices=change_reason_choice.choice,
    )
    change_comment = models.TextField(verbose_name=_('修改备注'), null=True, blank=True)

    class Meta:
        verbose_name = _('评价')
        verbose_name_plural = verbose_name


class CheckPhoto(models.Model):
    uploader = models.ForeignKey(
        UserBase,
        verbose_name=_("上传人"),
        on_delete=models.CASCADE,
        related_name='appraisal_check_photo',
    )
    apprid = models.ForeignKey(
        AppraisalInfo,
        verbose_name=_("评价"),
        on_delete=models.SET_NULL,
        related_name='check_photo',
        null=True,
    )
    upload_data = models.DateTimeField(auto_now_add=True, verbose_name=_('上传时间'))
    in_use = models.BooleanField(default=True, verbose_name=_('是否使用'))
    check_photo = models.ImageField(upload_to=settings.UPLOAD_CHECK_PHOTO, verbose_name=_('照片'))

    class Meta:
        verbose_name = _('评价照片')
        verbose_name_plural = verbose_name


class JsonSchemaOfAppraisal(models.Model):
    t1id = models.ForeignKey(
        ProductTypeL1,
        on_delete=models.CASCADE,
        related_name="json_schema_of_appraisal",
        unique=True,
    )
    json_schema = models.TextField()
    template_id = models.IntegerField(_("使用模板ID"), choices=template_choice.choice)
