# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.apps import apps
from rest_framework import serializers
from simplified_invite.models import InviteInfo
from simplified_invite.model_choices.invite_enum import i_status_choice
from logsys.models import LogInviteStatus
from usersys.models import UserBase
from usersys.model_choices.user_enum import role_choice
import json


HistoricalAppraisalInfo = apps.get_model('appraisalsys', 'HistoricalAppraisalInfo')


class AppraisalLogSerializer(serializers.ModelSerializer):
    formatted = serializers.SerializerMethodField()

    MAP_FIELD_NAME = {
        "final_total_price": "成交总金额为: {final_total_price} 元",
        "net_weight": "净重为: {net_weight} 吨",
        "pure_net_weight": "结算净重为: {pure_net_weight} 吨",
        "water_content": "含水量为: {water_content}%",
        "impurity_content": "杂质含量为: {impurity_content}吨",
        "tare": "扣重: {tare} 吨",
        "deduction_ratio": "扣杂比率: {deduction_ratio}",
    }

    MAP_PARAMETER_NAME = {
        "price_1": "质检员一报价: {price_1} 元/吨",
        "price_2": "质检员二报价: {price_2} 元/吨",
        "price_3": "质检员三报价: {price_3} 元/吨",
    }

    desc = '已完成，交易信息已由买方登记'

    class Meta:
        model = HistoricalAppraisalInfo
        fields = ('id', 'a_status', 'in_accordance', 'history_date', 'ivid', 'parameter', 'formatted')

    def get_formatted(self, obj):

        to_format = []
        to_format_args = {}
        for k, v in self.MAP_FIELD_NAME.items():
            attr = getattr(obj, k, None)
            # Fixme: How to determine if 0 should be contained in this format.
            if attr:
                to_format.append(v)
                to_format_args[k] = attr

        try:
            parameter = json.loads(obj.parameter)  # type: dict
        except ValueError:
            return None

        for k, v in self.MAP_PARAMETER_NAME.items():
            attr = parameter.get(k, None)
            # Fixme: How to determine if 0 should be contained in this format.
            if attr:
                to_format.append(v)
                to_format_args[k] = attr

        return _(
            "%s\n%s" %
            (self.desc, " ".join(to_format).format(**to_format_args))
        )


class InviteLogSerializer(serializers.ModelSerializer):
    formatted = serializers.SerializerMethodField()

    MAP_ISTATUS_DESCRIPTION = {
        i_status_choice.STARTED: "货品信息已由买方登记",
        i_status_choice.CANCELED: "买方取消",
        i_status_choice.SIGNED: "已完成，交易信息已由买方登记",
    }

    class Meta:
        model = LogInviteStatus
        fields = ('ivid', 'operator', 'log_date_time', 'i_status', 'formatted')

    def get_formatted(self, obj):
        # type: (InviteInfo) -> object
        return _(self.MAP_ISTATUS_DESCRIPTION.get(obj.i_status, None))


class InviteAndAppraisalLogSerializer(serializers.ModelSerializer):
    invite_logs = InviteLogSerializer(source='invite_log', many=True)
    appr_log = serializers.SerializerMethodField()

    class Meta:
        model = InviteInfo
        fields = ('invite_logs', 'appr_log')

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
