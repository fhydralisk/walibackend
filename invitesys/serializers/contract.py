from rest_framework import serializers
from invitesys.models import InviteContractSign


class ContractInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = InviteContractSign
        fields = ('id', 'ctid', 'generate_date', 'sign_status_A', 'sign_status_B', 'content')
        extra_kwargs = {
            'generate_date': {
                'format': '%s'
            }
        }

