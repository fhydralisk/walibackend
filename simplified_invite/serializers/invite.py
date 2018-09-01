from rest_framework import serializers
from simplified_invite.models import InviteInfo
from demandsys.serializers.validators.address_submit import AddressChoiceValidator


class DefaultInviterInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = InviteInfo
        # TODO select the field to display
        fields = ("price", "unit", "quantity", "aid", "street",)


class SelfInviteDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = InviteInfo
        # TODO: select the field to display
        fields = ('id', 'uid_s', 'uid_t')


class InviteDetailDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteInfo
        # TODO: select the field to display
        fields = ('id', 'uid_s', 'uid_t')


class InviteInfoDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model =InviteInfo
        # todo select the field to display
        fields = (
        "price", "unit", "quantity", "aid", "street",
        )


class InviteInfoInAppraisalSysSubmitSerializer(serializers.ModelSerializer):

    class Meta:
        model = InviteInfo
        # TODO select the field to seraializer the info submit by buyer
        fields = (
            'dmid_t',
            'quantity',
            'price',
            'unit',
            'aid',
            'street',
            'abid',
        )
        validators = [
            AddressChoiceValidator()
        ]
