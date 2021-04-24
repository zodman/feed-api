from rest_framework import routers
from .views import FeedView, EntryView


router = routers.SimpleRouter()
router.register(r'feed', FeedView)
router.register(r'entry', EntryView)
urlpatterns = router.urls
