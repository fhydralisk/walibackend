from rest_framework import serializers
from appraisalsys.models import AppraisalInfo


class AppraisalInfoDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalInfo
        fields = (
            "id", "final_price", "unit", "description", "quantity", "wcid", "qid",
        )


class AppraisalSubmitDisplaySerializer(AppraisalInfoDisplaySerializer):
    class Meta:
        model = AppraisalInfo
        fields = AppraisalInfoDisplaySerializer.Meta.fields + ("ivid",)
