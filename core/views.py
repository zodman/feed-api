from rest_framework import viewsets
from .models import Feed
from .serializers import FeedSerializer


class FeedView(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
