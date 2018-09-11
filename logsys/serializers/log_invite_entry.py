# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.apps import apps
from rest_framework import serializers
from invitesys.models import InviteInfo
from logsys.models import LogInviteStatus
from usersys.models import UserBase
from usersys.model_choices.user_enum import role_choice
import json

HistoricalAppraisalInfo = apps.get_model('appraisalsys', 'HistoricalAppraisalInfo')


class AppraisalLogSerializer(serializers.ModelSerializer):
    show = serializers.SerializerMethodField()

    class Meta:
        model = HistoricalAppraisalInfo
        fields = ('id', 'a_status', 'in_accordance', 'history_date', 'ivid', 'show')

    def get_show(self, obj):
        string = '成交总金额为：'
        string = string + str(obj.final_total_price) + '元 '
        string = string + '净重为：' + str(obj.net_weight) + '吨 '
        string = string + '结算净重为：' + str(obj.pure_net_weight) + '吨 '
        parameter = json.loads(obj.parameter)
        string = string + '质检员一报价：' + str(parameter['price_1']) + '元/吨 '
        string = string + '质检员二报价：' + str(parameter['price_2']) + '元/吨'
        return string


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
        fields = ('invite_logs', 'appr_log', 'description')

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

    def get_description(self, obj):
        # type: (InviteInfo) -> object
        return {
            'register': _('货品信息已由买方登记'),
            'finish': _('已完成，交易信息已由买方登记'),
            'cancel': _('买方取消'),
        }
