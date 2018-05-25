from rest_framework import serializers
from usersys.models import UserBase


class UserInfoSerialzier(serializers.ModelSerializer):
    validate_contact = serializers.ReadOnlyField(source='user_validate.contact')
    validate_company = serializers.ReadOnlyField(source='user_validate.company')
    validate_bankcard = serializers.ReadOnlyField(source='user_validate.bankcard')
    validate_obank = serializers.ReadOnlyField(source='user_validate.obank')
    validate_texno = serializers.ReadOnlyField(source='user_validate.texno')
    validate_address = serializers.ReadOnlyField(source='user_validate.address')
    validate_phonenum = serializers.ReadOnlyField(source='user_validate.phonenum')
    validate_t_user = serializers.ReadOnlyField(source='user_validate.t_user')
    validate_validate_status = serializers.ReadOnlyField(source='user_validate.validate_status')

    class Meta:
        model = UserBase
        fields = (
            'id', 'pn', 'role', 'register_date',
            'validate_contact', 'validate_company', 'validate_bankcard', 'validate_obank',
            'validate_texno', 'validate_address', 'validate_phonenum', 'validate_t_user',
            'validate_validate_status'
        )

        extra_kwargs = {
            "register_date": {
                "format": "%s"
            }
        }

