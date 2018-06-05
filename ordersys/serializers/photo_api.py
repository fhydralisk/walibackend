from rest_framework import serializers
from ordersys.models import OrderInfo


class UploadPhotoSerializer(serializers.Serializer):
    user_sid = serializers.CharField()
    oid = serializers.PrimaryKeyRelatedField(queryset=OrderInfo.objects, read_only=True)


class GetDeletePhotoSerializer(serializers.Serializer):
    user_sid = serializers.CharField()
    photo_id = serializers.IntegerField()
