from rest_framework import serializers

class SubmitAppraisalSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    ivid = serializers.IntegerField()
    in_accordance = serializers.BooleanField()
    parameter = serializers.JSONField(required=False)
    check_photos = serializers.ListField(child=serializers.IntegerField(min_value=1), required=False)
