import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
import django
django.setup()
from .models import Feed, Follow
from dramatiq.brokers.redis import RedisBroker
from dramatiq.brokers.stub import StubBroker
import dramatiq
import time
import logging

log = logging.getLogger(__name__)

if os.environ.get("TEST"):
    broker = StubBroker()
else:
    broker = RedisBroker(host='redis')

dramatiq.set_broker(broker)

def should_retry(retries_so_far, exception):
    return retries_so_far < 2

@dramatiq.actor(retry_when=should_retry)
def fetch_user_feed(id, user_id):
    feed = Feed.objects.get(id=id)
    log.info("executing fetch user_id")
    feed.fetch(user_id=user_id)


@dramatiq.actor
def fetch_feed(id):
    feed = Feed.objects.get(id=id)
    log.info("executing fetch")
    feed.fetch()

@dramatiq.actor
def fetch_all_feed():
    log.info("executing fetch_all_feed")
    follows = Follow.objects.all()
    for follow in follows:
        fetch_user_feed.send(id=follow.feed.id, user_id=follow.user.id)
