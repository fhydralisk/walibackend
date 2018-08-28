from rest_framework import serializers
from usersys.models import SearchHistory


class SearchHistorySubmitSerializer(serializers.ModelSerializer):
    user_sid = serializers.CharField(max_length=60)
    page = serializers.IntegerField(default=0)

    class Meta:
        model = SearchHistory
        fields = ('user_sid', 'keyword', 'page')


class GetSearchHistoryApiSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)


class SearchHistoryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ("keyword",)
