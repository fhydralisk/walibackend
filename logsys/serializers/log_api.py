from rest_framework import serializers
from ordersys.models import OrderProtocol, OrderInfo


class ObtainOrderLogSerializer(serializers.Serializer):
    user_sid = serializers.CharField()
    oid = serializers.PrimaryKeyRelatedField(queryset=OrderInfo.objects, read_only=True)


class ObtainOrderProtocolLogSerializer(serializers.Serializer):
    user_sid = serializers.CharField()
    opid = serializers.PrimaryKeyRelatedField(queryset=OrderProtocol.objects, read_only=True)
