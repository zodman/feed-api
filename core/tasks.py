"""
Async task using dramatiq

"""

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
    # for run on testing: TEST=1 python manage.py test
    broker = StubBroker()
else:
    broker = RedisBroker(host="redis")


class MiddlewareNotify(dramatiq.Middleware):
    """
        Small class for notify to the user about a error
        requirement of back-off mechanist
    """
    def after_process_message(self, *args, **kwargs):
        exception = kwargs.get("exception")
        if exception is not None:
            log.info(f":::: notify to user from a error {exception}")


broker.add_middleware(MiddlewareNotify())
dramatiq.set_broker(broker)


def should_retry(retries_so_far, exception):
    """
        Retry for two times or stop, after two continues failures ...
        requirement of back-off mechanist
    """
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
