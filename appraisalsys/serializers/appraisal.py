import json
import logging
from rest_framework import serializers
from appraisalsys.models import AppraisalInfo


logger = logging.getLogger(__name__)


class AppraisalInfoDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalInfo
        fields = (
            "id", "in_accordance", "parameter"
        )

    def to_representation(self, instance):
        # type: (AppraisalInfo) -> dict

        data = super(AppraisalInfoDisplaySerializer, self).to_representation(instance)
        try:
            parameter_dict = json.loads(data.get("parameter", "{}"))
        except ValueError:
            logger.warning('parameter of Pk: %d of AppraisalInfo object is invalid')
            parameter_dict = {}

        parameter_dict["water_content"] = instance.water_content
        parameter_dict["impurity_content"] = instance.impurity_content
        parameter_dict["final_total_price"] = instance.final_total_price
        parameter_dict["net_weight"] = instance.net_weight
        parameter_dict["pure_net_weight"] = instance.pure_net_weight

        data["parameter"] = parameter_dict
        return data


class AppraisalSubmitDisplaySerializer(AppraisalInfoDisplaySerializer):
    class Meta:
        model = AppraisalInfo
        fields = AppraisalInfoDisplaySerializer.Meta.fields + ("ivid", )
