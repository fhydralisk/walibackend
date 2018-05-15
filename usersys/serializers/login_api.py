from rest_framework import serializers
from usersys.models.user_enum import role_choice


class LoginSerializer(serializers.Serializer):
    pn = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=255)
    # vcode = serializers.CharField(max_length=5)
    role = serializers.ChoiceField(choices=role_choice.get_choices())


class LogoutSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    pn = serializers.CharField(max_length=20)
