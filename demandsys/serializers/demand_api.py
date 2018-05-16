from rest_framework import serializers
from usersys.models.user_enum import role_choice
from .demand import DemandPublishSerializer, DemandEditSerializer


class ObtainDemandSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    page = serializers.IntegerField(default=0)


class ObtainHotDemandSerializer(ObtainDemandSerializer):
    user_sid = serializers.CharField(max_length=60, default=None)
    role = serializers.ChoiceField(choices=role_choice.get_choices(), default=None)


class ObtainDemandDetailSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    id = serializers.IntegerField()


class PublishDemandSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    photo_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    demand = DemandPublishSerializer()


class EditDemandSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    id = serializers.IntegerField()
    photo_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    demand = DemandEditSerializer(partial=True, required=False)


class CloseDemandSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    id = serializers.IntegerField()
