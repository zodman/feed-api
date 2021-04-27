from rest_framework import serializers
from .models import Feed, Entry, ReadedEntry, Follow


class EntrySerializer(serializers.ModelSerializer):
    readed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Entry
        fields = [
            "id", "feed", "title", "link", "description", "pub_date", "readed"
        ]

    def get_readed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            try:
                return obj.entries_readed.filter(user=user).get().readed
            except ReadedEntry.DoesNotExist:
                return False
        return None


class FeedSerializer(serializers.ModelSerializer):
    follow = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Feed
        fields = ("id", "url", "last_fetch", "follow")
        read_only_fields = ("last_fetch", "follow", 'id')

    def get_follow(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            try:
                return obj.follows.filter(user=user).get().follow
            except Follow.DoesNotExist:
                return False
        return None
