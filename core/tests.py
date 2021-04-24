from test_plus.test import APITestCase
from django_seed import Seed
from .models import Feed, Entry, ReadedEntry


class ApiTest(APITestCase):
    def setUp(self):
        self.seeder = Seed.seeder()
        self.u1 = self.make_user("u1")

    def test_api(self):
        with self.subTest("Test creation feed and entry"):
            feed_url = 'https://www.nu.nl/rss/Algemeen'
            data = {
                'url': feed_url,
            }
            self.post("/api/feed/", data=data)
            self.response_201()
            id = self.last_response.json().get("id")
            self.assertTrue(Feed.objects.filter(url=feed_url).exists())
            self.get_check_200(f"/api/feed/{id}/")

            new_entry_data = {
                'raw': '<raw>',
                'feed': id,
                'title': self.seeder.faker.sentence(),
                'link': self.seeder.faker.url(),
                'description': self.seeder.faker.paragraph(),
                'pub_date': self.seeder.faker.date_time(),
            }
            self.post("/api/feed/{id}/entries/", data=new_entry_data)
            self.response_201()
            entry = Entry.objects.filter(feed=id)
            self.assertTrue(entry.exists())
            entry_id = self.last_response.json().get("id")
            self.assertEqual(entry_id, entry.first().id)
            self.get_check_200(f"/api/feed/{id}/entries/{entry_id}/")
            with self.subTest("Mark Entry readed") and self.login(
                    username='u1'):
                url =  f"/api/feed/{id}/entries/{entry_id}/readed/"
                self.get_check_200(url)
                entry = ReadedEntry.objects.get(entry=entry_id, user=self.u1)
                self.assertTrue(entry.readed)
