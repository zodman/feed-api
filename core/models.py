from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import urllib.request
import lxml.etree
import dateparser


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey("Feed", on_delete=models.CASCADE, related_name="follows")
    follow = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ("user", "feed")


class ReadedEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey(
        "Entry", on_delete=models.CASCADE, related_name="entries_readed"
    )
    readed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ("user", "entry")


class Entry(models.Model):
    feed = models.ForeignKey("Feed", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField()
    pub_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    def __str__(self):
        return f"Entry {self.id}"

    def _do_readed(self, user, readed=True):
        """ helper method for mark read and unread entry """
        readed_entry, created = ReadedEntry.objects.get_or_create(user=user, entry=self)
        readed_entry.readed = readed
        readed_entry.save()
        return readed_entry

    def mark_unreaded(self, user):
        return self._do_readed(user, readed=False)

    def mark_readed(self, user, readed=True):
        return self._do_readed(user, readed=True)


class Feed(models.Model):
    url = models.URLField(unique=True)
    last_fetch = models.DateTimeField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    def __str__(self):
        return f"Feed {self.id}"

    def follow(self, user):
        self._do_follow(user, follow=True)

    def unfollow(self, user):
        self._do_follow(user, follow=False)

    def _do_follow(self, user, follow=True):
        """ helper method for follow and unfollow feed """
        follow_obj, created = Follow.objects.get_or_create(user=user, feed=self)
        follow_obj.follow = follow
        follow_obj.save()
        return follow_obj

    def fetch(self, user_id=None):
        """ Method for download or fetch a feed and if you pass user the Reade
        entries will be created """
        resp = urllib.request.urlopen(self.url)
        root = lxml.etree.fromstring(resp.read())
        titles = root.xpath("//item/title/text()")
        links = root.xpath("//item/link/text()")
        descs = root.xpath("//item/description/text()")
        pub_dates = root.xpath("//item/pubDate/text()")
        raws = root.xpath("//item")
        elements = zip(*[titles, links, descs, pub_dates, raws])
        for title, link, desc, pub_date, raw in elements:
            date_ = dateparser.parse(pub_date)
            args = dict(
                title=title,
                feed=self,
                defaults=dict(link=link, description=desc, pub_date=date_),
            )
            entry, _ = Entry.objects.update_or_create(**args)
            if user_id is not None:
                ReadedEntry.objects.get_or_create(entry=entry, user_id=user_id)
        self.last_fetch = now()
        self.save()
