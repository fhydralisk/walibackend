from rest_framework import serializers
from ordersys.models import OrderProtocol, OrderInfo


class OrderLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderInfo
        fields = ('oid', 'operator', 'log_date_time', 'o_status')


class OrderProtocolLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProtocol
        fields = ('opid', 'operator', 'log_date_time', 'p_status', 'p_operate_status')
