from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey("Feed", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReadedEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey("Entry", on_delete=models.CASCADE)
    readed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'entry')


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

    def mark_readed(self, user):
        readed_entry, created = (ReadedEntry.objects
                                 .get_or_create(user=user, entry=self))
        readed_entry.readed = True
        readed_entry.save()
        return readed_entry


class Feed(models.Model):
    url = models.URLField(unique=True)
    last_fetch = models.DateTimeField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Feed {self.id}'
