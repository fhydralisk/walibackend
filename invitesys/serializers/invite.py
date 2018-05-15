from rest_framework import serializers
from invitesys.models import InviteInfo


class InviteInfoSubmitSerializer(serializers.ModelSerializer):

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
