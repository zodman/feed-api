from test_plus.test import APITestCase
from django_seed import Seed
from ..models import Feed, Entry, ReadedEntry, Follow
from faker import Faker

faker = Faker()


class FlowTest(APITestCase):
    def setUp(self):
        self.u1 = self.make_user("u1")

    def test_feed(self):
        urls = [
            "http://www.nu.nl/rss/Algemeen",
            "https://feeds.feedburner.com/tweakers/mixed",
        ]
        for url in urls:
            with self.subTest(url=url):
                feed = Feed(url=url)
                feed.save()
                feed.fetch()
        self.get_check_200("/api/feed/")
        resp = self.last_response.json()
        self.assertTrue(len(resp) == 2)
        for r in resp:
            with self.subTest(f"test entries {r}"):
                self.get_check_200(f"/api/feed/{r.get('id')}/entries/")

    def test_filter(self):
        seed = Seed.seeder()
        seed.orders = []
        seed.add_entity(Feed, 5, {"url": lambda x: seed.faker.unique.url()})
        seed.add_entity(Entry, 10)
        seed.execute()
        len_follow = 3
        self.feeds = list(Feed.objects.all().order_by("?"))[0:len_follow]
        for feed in self.feeds:
            Follow.objects.create(user=self.u1, feed=feed, follow=faker.boolean())
        entries = list(Entry.objects.all().order_by("?"))[0:5]
        for entry in entries:
            ReadedEntry.objects.create(
                user=self.u1, entry=entry, readed=faker.boolean()
            )
        self.assertTrue(ReadedEntry.objects.filter(readed=True).count() > 0)
        with self.subTest("check feed without auth"):
            self.get_check_200("/api/feed/")
            json_resp = self.last_response.json()
            self.assertTrue(len(json_resp) == 5, len(json_resp))

        with self.login(username="u1"):
            self.get_check_200("/api/feed/")
            json = self.last_response.json()
            self.assertTrue(len(json) == 5, len(json))
            for e in json:
                id = e.get("id")
                with self.subTest(f"feed for {id}"):
                    self.get_check_200(
                        f"/api/feed/{id}/entries/", data={"readed": True}
                    )
                    entries_json = self.last_response.json()
                    for i in entries_json:
                        with self.subTest(f"entries for {id}"):
                            self.assertTrue(i.get("readed"), i)

    def test_flow(self):
        with self.login(username="u1"):
            with self.subTest("Test creation feed and entry"):
                feed_url = "https://www.nu.nl/rss/Algemeen"
                data = {"url": feed_url}
                # Create a feed
                self.post("/api/feed/", data=data)
                self.response_201()
                id = self.last_response.json().get("id")
                self.assertTrue(Feed.objects.filter(url=feed_url).exists())
                follow = Follow.objects.get(user=self.u1, feed_id=id)
                self.assertTrue(follow)
                self.get_check_200(f"/api/feed/{id}/")
            with self.subTest("List feeds belongs to one feed"):
                seed = Seed.seeder()
                seed.add_entity(Entry, 10, {"feed": lambda x: Feed.objects.get(id=id)})
                seed.execute()
                self.get(f"/api/feed/{id}/entries/")
                self.response_200()
                entry = Entry.objects.filter(feed=id)
                self.assertTrue(entry.exists())
                entry_id = self.last_response.json()[0].get("id")
                self.assertTrue(entry_id)
                self.assertEqual(entry_id, entry.first().id)
                self.get_check_200(f"/api/feed/{id}/entries/{entry_id}/")
            with self.subTest("Mark Entry readed/unreaded"):
                url = f"/api/feed/{id}/entries/{entry_id}/readed/"
                self.get_check_200(url)
                entry = ReadedEntry.objects.get(entry=entry_id, user=self.u1)
                self.assertTrue(entry.readed)
                url = f"/api/feed/{id}/entries/{entry_id}/unreaded/"
                self.get_check_200(url)
                entry = ReadedEntry.objects.get(entry=entry_id, user=self.u1)
                self.assertFalse(entry.readed)
            with self.subTest("follow and unfollow feeds "):
                self.get_check_200(f"/api/feed/{id}/follow/")
                feed = Feed.objects.get(id=id)
                self.assertTrue(
                    (feed.follows.filter(user=self.u1, follow=True).exists())
                )
                self.get_check_200(f"/api/feed/{id}/unfollow/")
                feed = Feed.objects.get(id=id)
                self.assertTrue(
                    feed.follows.filter(user=self.u1, follow=False).exists()
                )
