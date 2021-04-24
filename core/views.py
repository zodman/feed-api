from rest_framework import viewsets
from .models import Feed, Entry
from .serializers import FeedSerializer, EntrySerializer


class EntryView(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class FeedView(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
