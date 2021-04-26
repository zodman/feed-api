from rest_framework import serializers
from .models import Feed, Entry, ReadedEntry


class EntrySerializer(serializers.ModelSerializer):
    readed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Entry
        fields = ["id", "title", "link", "description", "pub_date", "readed"]

    def get_readed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            try:
                return obj.readed.filter(user=user).get().readed
            except ReadedEntry.DoesNotExist:
                pass
        return False


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ("id", "url", "last_fetch")
        read_only_fields = ("last_fetch", )
