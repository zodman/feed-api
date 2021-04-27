from rest_framework_nested import routers
from .views import FeedView, EntryView, CompleteEntryView


router = routers.SimpleRouter()
router.register(r"feed", FeedView)
router.register(r"entries", CompleteEntryView)
entry_router = routers.NestedSimpleRouter(router, r"feed", lookup="feed")
entry_router.register(r"entries", EntryView, basename="feed-entries")
urlpatterns = router.urls + entry_router.urls
