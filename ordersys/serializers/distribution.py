from rest_framework import serializers
from ordersys.models import OrderLogisticsInfo


class OrderLogisticsInfoSubmitSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderLogisticsInfo
        exclude = ('id', 'oid', 'l_type', 'attach_datetime')


class OrderLogisticsInfoSerializer(serializers.ModelSerializer):
    expected_delivery_time = serializers.DateTimeField()

    class Meta:
        model = OrderLogisticsInfo
        fields = '__all__'
