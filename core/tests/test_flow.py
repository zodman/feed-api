from test_plus.test import APITestCase
from django_seed import Seed
from ..models import Feed, Entry, ReadedEntry, Follow
from faker import Faker

faker = Faker()


class FlowTest(APITestCase):

    def setUp(self):
        self.u1 = self.make_user("u1")

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
                new_entry_data = {
                    "raw": "<raw>",
                    "feed": id,
                    "title": faker.sentence(),
                    "link": faker.url(),
                    "description": faker.paragraph(),
                    "pub_date": faker.date_time(),
                }
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
            with self.subTest("follow and unfollow feeds "):
                self.get_check_200(f"/api/feed/{id}/follow/")
                feed = Feed.objects.get(id=id)
                self.assertTrue(feed.follow_set.exists())
