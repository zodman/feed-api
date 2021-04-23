from django.db import models


class Entry(models.Model):
    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField()
    pub_date = models.DateTimeField()
    raw = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Entry {self.id}'


class Feed(models.Model):
    url = models.URLField()
    last_fetch = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Feed {self.id}'
