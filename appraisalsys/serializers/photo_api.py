from rest_framework import serializers
from simplified_invite.models import InviteInfo


class UploadCheckPhotoSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    ivid = serializers.PrimaryKeyRelatedField(queryset=InviteInfo.objects)


class GetDeleteCheckPhotoSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    photo_id = serializers.IntegerField()
