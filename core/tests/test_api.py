from test_plus.test import APITestCase
from django_seed import Seed
from faker import Faker
from ..models import Feed, Entry, ReadedEntry, Follow

faker = Faker()


class ApiTest(APITestCase):
    def setUp(self):
        self.u2 = self.make_user("u2")
        seeder = Seed.seeder()
        seeder.add_entity(Feed, 50, {"url": lambda x: seeder.faker.unique.url()})
        seeder.add_entity(Entry, 500)
        seeder.execute()
        feeds = list(Feed.objects.all().order_by("?"))[0:30]
        self.feeds = feeds
        for feed in feeds:
            Follow.objects.create(user=self.u2, feed=feed, follow=faker.boolean())
        entries = list(Entry.objects.all().order_by("?"))[0:450]
        for entry in entries:
            ReadedEntry.objects.create(
                user=self.u2, entry=entry, readed=faker.boolean()
            )

    def test_list_feed(self):
        self.get("/api/feed/")
        self.response_200()
        json = self.last_response.json()
        self.assertTrue(len(json) > 0, len(json))
        entries = Entry.objects.filter(feed=self.feeds[0].id)
        self.assertTrue(entries.exists())
