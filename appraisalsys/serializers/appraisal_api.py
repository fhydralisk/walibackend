from rest_framework import serializers
from demandsys.models import ProductWaterContent
from appraisalsys.models import ImpurityContent


class CommonFieldAppraisalSerializer(serializers.Serializer):
    final_total_price = serializers.FloatField(min_value=0.0)
    net_weight = serializers.FloatField(min_value=0.0)
    pure_net_weight = serializers.FloatField(min_value=0.0)
    wcid = serializers.PrimaryKeyRelatedField(
        queryset=ProductWaterContent.objects.filter(in_use=True),
        allow_null=True,
        default=None,
    )
    impcid = serializers.PrimaryKeyRelatedField(
        queryset=ImpurityContent.objects.filter(in_use=True),
        allow_null=True,
        default=None,
    )


class SubmitAppraisalSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    ivid = serializers.IntegerField()
    in_accordance = serializers.BooleanField()
    parameter = serializers.JSONField()
    check_photos = serializers.ListField(child=serializers.IntegerField(min_value=1), required=False)

    def validate(self, attrs):
        seri_parameter = CommonFieldAppraisalSerializer(data=attrs['parameter'])
        seri_parameter.is_valid(raise_exception=True)
        return attrs
