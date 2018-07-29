from rest_framework import serializers
from usersys.models import UserFeedback


class FeedbackApiSerializer(serializers.ModelSerializer):
    user_sid = serializers.CharField()

    class Meta:
        model = UserFeedback
        fields = ('user_sid', 'content', 'wechat_id')
