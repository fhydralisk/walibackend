import datetime
from rest_framework import serializers
from ordersys.models import OrderLogisticsInfo


class OrderLogisticsInfoSubmitSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderLogisticsInfo
        exclude = ('id', 'oid', 'l_type', 'attach_datetime')


class TimeShiftField(serializers.DateTimeField):
    def __init__(self, ref, *args, **kwargs):
        super(TimeShiftField, self).__init__(*args, **kwargs)
        self.ref = ref

    def to_representation(self, value):
        if self.parent.instance is not None:
            value = value + datetime.timedelta(days=getattr(self.parent.instance, self.ref))
        return super(TimeShiftField, self).to_representation(value)


class OrderLogisticsInfoSerializer(serializers.ModelSerializer):

    expected_arrival_time = TimeShiftField(source='attach_datetime', ref='delivery_days')

    class Meta:
        model = OrderLogisticsInfo
        fields = '__all__'

