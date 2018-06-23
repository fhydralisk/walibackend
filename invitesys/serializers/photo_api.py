from rest_framework import serializers
from invitesys.models import InviteInfo


class UploadPhotoSerializer(serializers.Serializer):
    user_sid = serializers.CharField()
    ivid = serializers.PrimaryKeyRelatedField(queryset=InviteInfo.objects, required=False)
    photo_desc = serializers.CharField(allow_blank=True)


class GetDeletePhotoSerializer(serializers.Serializer):
    user_sid = serializers.CharField()
    photo_id = serializers.IntegerField()
