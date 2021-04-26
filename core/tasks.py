import dramatiq
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
import django
django.setup()
from .models import Feed

from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(host='redis')
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def fetch_feed(id):
    feed = Feed.objects.get(id=id)
    feed.fetch()

@dramatiq.actor
def fetch_all_feed():
    feeds = Feed.objects.all()
    for feed in feeds:
        fetch_feed.send(id=feed.id)
