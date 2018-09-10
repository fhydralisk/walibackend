# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.apps import apps
from rest_framework import serializers
from invitesys.models import InviteInfo
from logsys.models import LogInviteStatus
from usersys.models import UserBase
from usersys.model_choices.user_enum import role_choice


HistoricalAppraisalInfo = apps.get_model('appraisalsys', 'HistoricalAppraisalInfo')


class AppraisalLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalAppraisalInfo
        fields = '__all__'


class InviteLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogInviteStatus
        fields = ('ivid', 'operator', 'log_date_time', 'i_status')


class InviteAndAppraisalLogSerializer(serializers.ModelSerializer):
    invite_logs = InviteLogSerializer(source='invite_log', many=True)
    appr_log = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = InviteInfo
        fields = ('invite_logs', 'appri_log', 'description')

    def __init__(self, user=None, *args, **kwargs):
        # type: (UserBase, list, dict) -> None
        super(InviteAndAppraisalLogSerializer, self).__init__(*args, **kwargs)
        self._user = user

    def get_appr_log(self, obj):
        # type: (InviteInfo) -> object
        if self._user is not None and self._user.role == role_choice.BUYER:
            try:
                return AppraisalLogSerializer(
                    instance=HistoricalAppraisalInfo.objects.filter(ivid=obj).latest('history_date')
                ).data
            except HistoricalAppraisalInfo.DoesNotExist:
                return None
        else:
            return None

    def get_description_field(self, obj):
        # type: (InviteInfo) -> object
        return {
            'register': _('货品信息已由买方登记'),
            'finish': _('已完成，交易信息已由买方登记'),
            'cancel': _('买方取消'),
        }
