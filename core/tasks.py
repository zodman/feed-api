import dramatiq
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
import django
django.setup()
from dramatiq.brokers.redis import RedisBroker
from .models import Feed

redis_broker = RedisBroker(host='redis')
dramatiq.set_broker(redis_broker)

@dramatiq.actor
def fetch_user_feed(id, user_id):
    feed = Feed.objects.get(id=id)
    print("executing fetch user_id")
    feed.fetch(user_id=user_id)



@dramatiq.actor
def fetch_feed(id):
    feed = Feed.objects.get(id=id)
    print("executing fetch")
    feed.fetch()

@dramatiq.actor
def fetch_all_feed():
    print("executing fetch_all_feed")
    feeds = Feed.objects.all()
    for feed in feeds:
        fetch_feed.send(id=feed.id)
