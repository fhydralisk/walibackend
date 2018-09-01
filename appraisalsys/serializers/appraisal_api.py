from rest_framework import serializers
from appraisalsys.models import AppraisalInfo


class SubmitAppraisalSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    ivid = serializers.IntegerField()
    parameter = serializers.JSONField()

    def validate(self, attrs):
        seri_cls = AppraisalInfoSubmitSerializer
        seri = seri_cls(data=attrs["parameter"])
        seri.is_valid(raise_exception=True)
        return attrs


class AppraisalInfoSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalInfo
        # todo select the fields to validate the parameter
        fields = (
            "some_fields",
        )
