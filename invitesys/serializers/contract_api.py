from rest_framework import serializers
from invitesys.model_choices.contract_enum import sign_method_choice


class ObtainContractInfoSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    cid = serializers.IntegerField()


class SignContractSerializer(ObtainContractInfoSerializer):
    sign_method = serializers.ChoiceField(sign_method_choice.get_choices())
