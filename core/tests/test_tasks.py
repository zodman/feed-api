from django.test import TransactionTestCase
from dramatiq import Worker
from django.contrib.auth.models import User
from ..models import Feed, Follow
from ..tasks import fetch_user_feed, broker


class TestCase(TransactionTestCase):
    def setUp(self):
        self.broker = broker
        self.broker.emit_after("process_boot")
        self.broker.flush_all()
        self.worker = Worker(self.broker, worker_timeout=100)
        self.worker.start()
        self.u = User.objects.create(username='u1')


    def test_back_off_case(self):
        url= "http://localhost"
        feed = Feed(url=url)
        feed.save()
        fetch_user_feed.send(id=feed.id, user_id = self.u.id)
        with self.assertRaises(Exception):
            self.broker.join(fetch_user_feed.queue_name,fail_fast=True)
            self.worker.join()
