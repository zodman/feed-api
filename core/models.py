from django.db import models
from django.utils.timezone import now


class Feed(models.Model):
    url = models.URLField()
    last_fetch = models.DateTimeField(default=now)

    def __str__(self):
        return f'Feed {self.id}'
