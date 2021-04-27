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
    pass


class EntryFilter(filters.FilterSet):
    CHOICES = ((True, "Yes"), (False, "No"))
    readed = filters.ChoiceFilter(method="filter_readed",label="readed",
                                  choices=CHOICES)

    class Meta:
        model = Entry
        fields = ("link", "title", "readed")

    def filter_readed(self, queryset, name, value):
        return queryset.filter(entries_readed__readed=value)


class CompleteEntryView(viewsets.ReadOnlyModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_backends = (filters.DjangoFilterBackend,rest_filters.OrderingFilter)
    filterset_class = EntryFilter
    ordering_fields = ("pub_date",)
    permission_classes = [IsAuthenticated]



class EntryView(MixFeed):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_backends = (filters.DjangoFilterBackend,rest_filters.OrderingFilter)
    filterset_class = EntryFilter
    ordering_fields = ("pub_date",)

    def get_queryset(self):
        qs = super().get_queryset()
        if "feed_pk" in self.kwargs:
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

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def perform_create(self, serializer):
        feed = serializer.save()
        if self.request.user.is_authenticated:
            user = self.request.user
            Follow.objects.create(user=user, feed=feed)
        fetch_feed.send(id=feed.id)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def fetch(self, request, *args,**kwargs):
        feed = self.get_object()
        user = request.user
        fetch_user_feed.send(id=feed.id, user_id=user.id)
        return Response(data="ok")

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def unfollow(self, request, *args, **kwargs):
        self._fetch_follow(request, follow=False)
        return self.retrieve(request)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def follow(self, request, *args, **kargs):
        self._fetch_follow(request, follow=True)
        return self.retrieve(request)

    def _fetch_follow(self, request, follow=True):
        feed = self.get_object()
        if follow:
            feed.follow(user=request.user)
        else:
            feed.unfollow(user=request.user)
