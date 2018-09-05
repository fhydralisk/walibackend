from rest_framework import serializers
from usersys.model_choices.user_enum import role_choice
from demandsys.model_choices.demand_enum import match_order_choice
from .demand import DemandPublishSerializer, DemandEditSerializer


class ObtainDemandSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    page = serializers.IntegerField(default=0)
    t1id = serializers.IntegerField(default=None, allow_null=True)
    aid = serializers.IntegerField(default=None, allow_null=True)
    asc_of_price = serializers.NullBooleanField(default=None)
    count_per_page = serializers.IntegerField(default=3)


class ObtainHotDemandSerializer(ObtainDemandSerializer):
    user_sid = serializers.CharField(max_length=60, default=None, allow_null=True)
    role = serializers.ChoiceField(choices=role_choice.get_choices(), default=None, allow_null=True)
    count_per_page = serializers.IntegerField(default=6)


class ObtainDemandDetailSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    id = serializers.IntegerField()


class ObtainDemandMatchSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    id = serializers.IntegerField()
    order = serializers.ChoiceField(choices=match_order_choice.get_choices())
    asc = serializers.BooleanField()
    page = serializers.IntegerField(min_value=0, default=0)


class PublishDemandSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    photo_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    demand = DemandPublishSerializer()


class EditDemandSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    id = serializers.IntegerField()
    photo_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    demand = DemandEditSerializer(partial=True, required=False)


class CloseDeleteDemandSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    id = serializers.IntegerField()


class ObtainSearchSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    keyword = serializers.CharField(max_length=256)
    page = serializers.IntegerField(default=0)
    t1id = serializers.IntegerField(default=None, allow_null=True)
    aid = serializers.IntegerField(default=None, allow_null=True)
    asc_of_price = serializers.NullBooleanField(default=None)
