from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from .models import Feed, Entry
from .serializers import FeedSerializer, EntrySerializer


class MixFeed(mixins.CreateModelMixin, mixins.ListModelMixin,
              mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass

class EntryView(MixFeed):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


    @action(detail=True, methods=["get"])
    def readed(self, request, **kwargs):
        entry = self.get_object()
        entry.mark_readed(user=request.user)
        return self.retrieve(request)


class FeedView(MixFeed):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer


