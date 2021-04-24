from rest_framework import viewsets
from rest_framework import mixins
from .models import Feed, Entry
from .serializers import FeedSerializer, EntrySerializer


class MixFeed(mixins.CreateModelMixin, mixins.ListModelMixin,
              mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass

class EntryView(MixFeed):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class FeedView(MixFeed):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer


