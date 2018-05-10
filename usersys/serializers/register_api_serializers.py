from rest_framework import serializers
from usersys.models import UserBase
from base.util.misc_validators import validators


class PNSubmitSerializer(serializers.Serializer):
    pn = serializers.CharField(max_length=20, validators=[validators.get_validator("phone number")])


class PNFinalRegisterSerializer(serializers.ModelSerializer):
    sid = serializers.CharField(max_length=60)

    class Meta:
        model = UserBase
        fields = ('pn', 'role', 'password', 'sid')
        extra_kwargs = {
            'pn': {
                'validators': []
            }
        }


class PNValidateSerializer(serializers.Serializer):
    pn = serializers.CharField(max_length=20)
    sid = serializers.CharField(max_length=60)
    vcode = serializers.CharField(max_length=6)


class ResetPasswordSerializer(serializers.ModelSerializer):
    sid = serializers.CharField(max_length=60)
    vcode = serializers.CharField(max_length=6)
    pn = serializers.CharField(validators=[validators.get_validator("phone number")])

    class Meta:
        model = UserBase
        fields = ('pn', 'role', 'password', 'sid', 'vcode')
