from test_plus.test import APITestCase
from django_seed import Seed
from .models import Feed, Entry, ReadedEntry, Follow


class ApiTest(APITestCase):
    def setUp(self):
        self.seeder = Seed.seeder()
        self.u1 = self.make_user("u1")

    def test_list_feed(self):
        self.seeder.add_entity(Feed, 1)
        self.seeder.add_entity(Entry, 10)
        self.seeder.execute()
        self.get("/api/feed/")
        self.response_200()
        json = self.last_response.json()
        self.assertTrue(len(json) == 1)
        entries = Entry.objects.filter(feed=json[0].get("id"))
        self.assertTrue(entries.exists())
        for i in json:
            with self.subTest(f"test entries {i}"):
                self.get_check_200(f"/api/feed/{i.get('id')}/entries/")

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
                new_entry_data = {
                    "raw": "<raw>",
                    "feed": id,
                    "title": self.seeder.faker.sentence(),
                    "link": self.seeder.faker.url(),
                    "description": self.seeder.faker.paragraph(),
                    "pub_date": self.seeder.faker.date_time(),
                }
            with self.subTest("List feeds belongs to one feed"):
                # list feed items belongs to one feed
                self.post("/api/feed/{id}/entries/", data=new_entry_data)
                self.response_201()
                entry = Entry.objects.filter(feed=id)
                self.assertTrue(entry.exists())
                entry_id = self.last_response.json().get("id")
                self.assertEqual(entry_id, entry.first().id)
                self.get_check_200(f"/api/feed/{id}/entries/{entry_id}/")

            with self.subTest("Mark Entry readed"):
                url = f"/api/feed/{id}/entries/{entry_id}/readed/"
                self.get_check_200(url)
                entry = ReadedEntry.objects.get(entry=entry_id, user=self.u1)
                self.assertTrue(entry.readed)
                url = f"/api/feed/{id}/entries/{entry_id}/unreaded/"
                self.get_check_200(url)
                entry = ReadedEntry.objects.get(entry=entry_id, user=self.u1)
                self.assertFalse(entry.readed)
            with self.subTest(" follow and unfollow feeds "):
                self.get_check_200("/api/feed/{id}/follow")
                feed = Feed.objects.get(id=id)
                self.assertTrue(feed.follow_set.exists())

    def test_filter_feeds(self):
        self.seeder.add_entity(Feed, 100)
        self.seeder.add_entity(Entry, 500)
        self.seeder.add_entity(Follow, 150)
        self.seeder.add_entity(ReadedEntry, 450)
        self.seeder.execute()
