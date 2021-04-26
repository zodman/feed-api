from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from .models import Feed, Entry, Follow
from .serializers import FeedSerializer, EntrySerializer


class MixFeed(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass


class EntryFilter(filters.FilterSet):
    readed = filters.BooleanFilter(method="filter_readed")
    class Meta:
        model = Entry
        fields = ("link", "title", "readed")


    def filter_readed(self, queryset, name,value):
        kwargs = {
            f'readed__{name}': value
        }
        return queryset.filter(**kwargs)




class EntryView(MixFeed):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_backends = ( filters.DjangoFilterBackend,)
    filterset_class = EntryFilter

    @action(detail=True, methods=["get"])
    def readed(self, request, **kwargs):
        entry = self.get_object()
        if request.user.is_authenticated:
            entry.mark_readed(user=request.user)
        return self.retrieve(request)

    @action(detail=True, methods=["get"])
    def unreaded(self, request, **kwargs):
        entry = self.get_object()
        if request.user.is_authenticated:
            entry.mark_unreaded(user=request.user)
        return self.retrieve(request)


class FeedView(mixins.CreateModelMixin, MixFeed):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            user = self.request.user
            qs = qs.filter(follows__user=user)
        return qs

    def perform_create(self, serializer):
        feed = serializer.save()
        if self.request.user.is_authenticated:
            user = self.request.user
            Follow.objects.create(user=user, feed=feed)

    @action(detail=True, methods=["get"])
    def unfollow(self, request, *args, **kwargs):
        self._fetch_follow(request, follow=False)
        return self.retrieve(request)

    @action(detail=True, methods=["get"], name="Follow Feed")
    def follow(self, request, *args, **kargs):
        self._fetch_follow(request, follow=True)
        return self.retrieve(request)

    def _fetch_follow(self, request, follow=True):
        feed = self.get_object()
        if request.user.is_authenticated:
            if follow:
                feed.follow(user=request.user)
            else:
                feed.unfollow(user=request.user)
