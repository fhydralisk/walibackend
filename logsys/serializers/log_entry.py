from rest_framework import serializers
from logsys.models import LogOrderStatus, LogOrderProtocolStatus
from django.apps import apps


class OrderLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogOrderStatus
        fields = ('oid', 'operator', 'log_date_time', 'o_status')


class OrderProtocolLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogOrderProtocolStatus
        fields = ('opid', 'operator', 'log_date_time', 'p_status', 'p_operate_status')


class AppraisalLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = apps.get_model('appraisalsys', 'HistoricalAppraisalInfo')
        fields = '__all__'
