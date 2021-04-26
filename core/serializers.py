from rest_framework import serializers
from .models import Feed, Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = "__all__"


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ("id", "url", "last_fetch")
        read_only_fields = ("last_fetch",)
