from rest_framework import serializers
from base.util.timestamp import datetime_to_timestamp
from invitesys.models import InviteContractSign


class ContractInfoSerializer(serializers.ModelSerializer):

    generate_date = serializers.SerializerMethodField()

    class Meta:
        model = InviteContractSign
        fields = ('id', 'ctid', 'generate_date', 'sign_status_A', 'sign_status_B', 'content')

    def get_generate_date(self, obj):
        return int(datetime_to_timestamp(obj.generate_date))

