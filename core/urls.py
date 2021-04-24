from rest_framework_nested import routers
from .views import FeedView, EntryView



router = routers.SimpleRouter()
router.register(r'feed', FeedView)
entry_router = routers.NestedSimpleRouter(router, r'feed', lookup='feed')
entry_router.register(r'entries', EntryView, basename='feed-entries')
urlpatterns = router.urls + entry_router.urls
