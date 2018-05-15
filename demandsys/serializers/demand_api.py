from rest_framework import serializers
from usersys.models.user_enum import role_choice


class ObtainDemandSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    page = serializers.IntegerField(default=0)


class ObtainHotDemandSerializer(ObtainDemandSerializer):
    user_sid = serializers.CharField(max_length=60, default=None)
    role = serializers.ChoiceField(choices=role_choice.get_choices(), default=None)


class ObtainDemandDetailSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    id = serializers.IntegerField()
