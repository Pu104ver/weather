from rest_framework import serializers
from weather.models import SearchHistory, CityStat


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ["id", "user", "session_key", "city", "searched_at"]
        read_only_fields = ["user", "session_key", "searched_at"]


class CityStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityStat
        fields = ["city", "count"]
