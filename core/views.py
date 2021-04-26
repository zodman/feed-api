from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from .models import Feed, Entry, Follow
from .serializers import FeedSerializer, EntrySerializer


class MixFeed(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class EntryView(MixFeed):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    @action(detail=True, methods=["get"])
    def readed(self, request, **kwargs):
        entry = self.get_object()
        entry.mark_readed(user=request.user)
        return self.retrieve(request)

    @action(detail=True, methods=["get"])
    def unreaded(self, request, **kwargs):
        entry = self.get_object()
        entry.mark_unreaded(user=request.user)
        return self.retrieve(request)


class FeedView(MixFeed):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    def perform_create(self, serializer):
        feed = serializer.save()
        if self.request.user.is_authenticated:
            user = self.request.user
            Follow.objects.create(user=user, feed=feed)

    @action(detail=True, methods=["get"])
    def unfollow(self, request, *args, **kwargs):
        self._fetch_follow(follow=False)

    @action(detail=True, methods=["get"])
    def follow(self, request, *args, **kargs):
        self._fetch_follow(follow=True)

    def _fetch_follow(self, request, follow=True):
        feed = self.get_object()
        if request.user.is_authenticated:
            user = request.user
            follow_obj, created = Follow.objects.get_or_create(user, feed=feed)
            follow_obj.follow = follow
            follow_obj.save()
