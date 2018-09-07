from rest_framework import serializers
from appraisalsys.models import AppraisalInfo


class AppraisalInfoDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalInfo
        fields = (
            "id", "in_accordance", "final_total_price", "description", "net_weight", "pure_net_weight", "wcid", "impcid",
            "price_1", "price_2", "price_3",
        )


class AppraisalSubmitDisplaySerializer(AppraisalInfoDisplaySerializer):
    class Meta:
        model = AppraisalInfo
        fields = AppraisalInfoDisplaySerializer.Meta.fields + ("ivid",)
