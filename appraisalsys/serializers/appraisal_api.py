from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CommonFieldAppraisalSerializer(serializers.Serializer):
    final_price = serializers.FloatField(min_value=0.0)
    net_weight = serializers.FloatField(min_value=0.0)
    tare = serializers.FloatField(min_value=0.0, allow_null=True, default=None)
    deduction_ratio = serializers.FloatField(min_value=0.0, max_value=100, default=None, allow_null=True)
    water_content = serializers.FloatField(allow_null=True, default=None, min_value=0.0, max_value=100)


class SubmitAppraisalSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    ivid = serializers.IntegerField()
    in_accordance = serializers.BooleanField()
    parameter = serializers.JSONField()
    check_photos = serializers.ListField(child=serializers.IntegerField(min_value=1), required=False)

    def validate(self, attrs):
        if not attrs['in_accordance']:
            if not "tare" in attrs['parameter'] and not "deduction_ratio" in attrs['parameter']:
                raise ValidationError("Either tare or deduction_ratio must be set", 400)
            seri_parameter = CommonFieldAppraisalSerializer(data=attrs['parameter'])
            seri_parameter.is_valid(raise_exception=True)
        return attrs
