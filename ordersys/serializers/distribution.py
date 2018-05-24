from rest_framework import serializers
from ordersys.models import OrderLogisticsInfo


class OrderLogisticsInfoSubmitSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderLogisticsInfo
        exclude = ('id', 'oid', 'l_type', 'attach_datetime')
