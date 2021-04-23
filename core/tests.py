from test_plus.test import APITestCase
from django_seed import Seed
from .models import Feed


class ApiTest(APITestCase):
    @classmethod
    def setUpData(cls):
        seeder = Seed.seeder()
        seeder.add_entity(Feed, 5)
        seeder.execute()

    def test_api(self):

        self.get("/api/feed/")
        self.response_200()
        feed_url = 'https://www.nu.nl/rss/Algemeen'
        data = {
            'url':feed_url,
        }
        self.post("/api/feed/", data=data)
        self.response_201()
        print(self.last_response.content)
        self.assertTrue(Feed.objects.filter(url=feed_url).exists())
