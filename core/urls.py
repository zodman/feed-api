from rest_framework import routers
from .views import FeedView


router = routers.SimpleRouter()
router.register(r'feed', FeedView)
urlpatterns = router.urls
