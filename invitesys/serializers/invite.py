from rest_framework import serializers
from invitesys.models import InviteInfo
from demandsys.serializers.validators.address_submit import AddressChoiceValidator


class BuyerInviteInfoSubmitSerializer(serializers.ModelSerializer):

    class Meta:
        model = InviteInfo
        fields = (
            'dmid_s',
            'dmid_t',
            'quantity',
            'price',
            'unit',
            'pmid',
            'disid',
            'dis_duration',
            'aid',
            'street',
            'abid',
        )

        validators = [
            AddressChoiceValidator()
        ]


class SellerInviteInfoSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteInfo
        fields = (
            'dmid_s',
            'dmid_t',
            'quantity',
            'price',
            'unit',
            'pmid',
            'disid',
            'dis_duration',
        )
