from rest_framework.serializers import ModelSerializer
from usersys.models.usermodel import UserValidate, UserValidateArea
from .validators.validate_validator import UserValidateStatusValidator, UserValidateTUserValidator


class UserValidateUserSerializer(ModelSerializer):
    class Meta:
        model = UserValidate
        fields = '__all__'
        read_only_fields = ('id', 'uid')
        extra_kwargs = {
            "validate_status": {
                "validators": [UserValidateStatusValidator(is_user=True)]
            },
            "t_user": {
                "validators": [UserValidateTUserValidator(is_user=True)]
            }
        }


class UserValidateAreaSerializer(ModelSerializer):
    class Meta:
        model = UserValidateArea
        fields = '__all__'

