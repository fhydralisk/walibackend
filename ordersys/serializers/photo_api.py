from rest_framework import serializers
from ordersys.models import OrderInfo
from ordersys.model_choices.photo_enum import photo_type_choice


class UploadPhotoSerializer(serializers.Serializer):
    user_sid = serializers.CharField()
    oid = serializers.PrimaryKeyRelatedField(queryset=OrderInfo.objects)
    t_photo = serializers.ChoiceField(choices=photo_type_choice.get_choices())


class GetDeletePhotoSerializer(serializers.Serializer):
    user_sid = serializers.CharField()
    photo_id = serializers.IntegerField()
