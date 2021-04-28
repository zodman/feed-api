from rest_framework import viewsets, filters as rest_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django.db.models import OuterRef, Subquery, Func
from .models import Feed, Entry, Follow, ReadedEntry
from .serializers import FeedSerializer, EntrySerializer
from .tasks import fetch_feed, fetch_user_feed


class MixFeed(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """ Empty mixing only for List and retreive """
    pass


class EntryFilter(filters.FilterSet):
    CHOICES = ((True, "Yes"), (False, "No"))
    readed = filters.ChoiceFilter(
        method="filter_readed", label="readed", choices=CHOICES
    )

    class Meta:
        model = Entry
        fields = ("link", "title", "readed")

    def filter_readed(self, queryset, name, value):
        return queryset.filter(entries_readed__readed=value)


class CompleteEntryView(viewsets.ReadOnlyModelViewSet):
    """
        View for view all global entries of feeds
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_backends = (filters.DjangoFilterBackend, rest_filters.OrderingFilter)
    filterset_class = EntryFilter
    ordering_fields = ("pub_date",)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.filter(feed__follows__user=user)
        return qs


class EntryView(MixFeed):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_backends = (filters.DjangoFilterBackend, rest_filters.OrderingFilter)
    filterset_class = EntryFilter
    ordering_fields = ("pub_date",)

    def get_queryset(self):
        """ filter al entries by the one feed from url """
        qs = super().get_queryset()
        qs = qs.filter(feed=self.kwargs["feed_pk"])
        return qs

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def readed(self, request, **kwargs):
        entry = self.get_object()
        e = entry.mark_readed(user=request.user)
        return self.retrieve(request)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def unreaded(self, request, **kwargs):
        entry = self.get_object()
        entry.mark_unreaded(user=request.user)
        return self.retrieve(request)


class FeedView(mixins.CreateModelMixin, MixFeed):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    def perform_create(self, serializer):
        """ post created action, create a follow for the feed """
        feed = serializer.save()
        if self.request.user.is_authenticated:
            user = self.request.user
            Follow.objects.create(user=user, feed=feed)
        fetch_feed.send(id=feed.id)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def fetch(self, request, *args, **kwargs):
        """ action for fetch the feed
        """
        feed = self.get_object()
        user = request.user
        fetch_user_feed.send(id=feed.id, user_id=user.id)
        return Response(data="ok")

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def unfollow(self, request, *args, **kwargs):
        """ unfollow the feed """
        self._fetch_follow(request, follow=False)
        return self.retrieve(request)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def follow(self, request, *args, **kargs):
        """ follow the feed """
        self._fetch_follow(request, follow=True)
        return self.retrieve(request)

    def _fetch_follow(self, request, follow=True):
        feed = self.get_object()
        if follow:
            feed.follow(user=request.user)
        else:
            feed.unfollow(user=request.user)
