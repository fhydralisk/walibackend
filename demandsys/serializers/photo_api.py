from rest_framework import serializers


class UploadPhotoSerializer(serializers.Serializer):
    dmid = serializers.IntegerField(required=False)
    user_sid = serializers.CharField(max_length=60)


class RemovePhotoSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    id = serializers.IntegerField()


class GetPhotoSerializer(serializers.Serializer):
    dmid = serializers.IntegerField()
