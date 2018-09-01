from rest_framework import serializers
from appraisalsys.models import AppraisalInfo


class AppraisalSubmitDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalInfo
        # TODO select the field to display when submit susseed
        fields = (
            "some fields",
        )
