from test_plus.test import APITestCase
from django_seed import Seed
from .models import Feed, Entry


class ApiTest(APITestCase):
    # @classmethod
    # def setUpData(cls):
        # seeder = Seed.seeder()
        # seeder.add_entity(Feed, 5)
        # seeder.add_entity(Entry, 20)
        # seeder.execute()

    def setUp(self):
        self.seeder = Seed.seeder()

    def test_api_get(self):
        self.get_check_200("/api/feed/")
        self.get_check_200("/api/entry/")

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

            new_entry_data = {
                'raw': '<raw>',
                'feed': id,
                'title': self.seeder.faker.sentence(),
                'link': self.seeder.faker.url(),
                'description': self.seeder.faker.paragraph(),
                'pub_date': self.seeder.faker.date_time(),
            }
            self.post("/api/entry/", data=new_entry_data)
            self.response_201()
            entry = Entry.objects.filter(feed=id)
            self.assertTrue(entry.exists())
            self.assertEqual(self.last_response.json().get("id"), entry.first().id)

