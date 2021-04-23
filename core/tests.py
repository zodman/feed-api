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

        self.get("/api/feed")
        self.response_200()
