from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import requests
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
    entry = models.ForeignKey("Entry", on_delete=models.CASCADE, related_name="readed")
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
    raw = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    def __str__(self):
        return f"Entry {self.id}"

    def _do_readed(self, user, readed=True):
        readed_entry, created = ReadedEntry.objects.get_or_create(user=user, entry=self)
        readed_entry.readed = readed
        readed_entry.save()
        return readed_entry

    def mark_unreaded(self, user):
        self._do_readed(user, readed=False)

    def mark_readed(self, user, readed=True):
        self._do_readed(user, readed=True)




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
        follow_obj, created = Follow.objects.get_or_create(user, feed=self)
        follow_obj.follow = follow
        follow_obj.save()
        return follow_obj

    def fetch(self):
        resp = requests.get(self.url)
        root = lxml.etree.fromstring(resp.content)
        titles = root.xpath("//title/text()")
        links = root.xpath("//link/text()")
        descs = root.xpath("//description/text()")
        pub_dates = root.xpath("//pubDate/text()")
        raws = root.xpath("//item")
        elements = zip(*[titles, links, descs, pub_dates, raws])
        for title, link, desc, pub_date, raw in elements:
            raw_ = lxml.etree.tostring(raw).decode("utf-8")
            date_ = dateparser.parse(pub_date) 
            Entry.objects.get_or_create(title=title, link=link,
                                        feed = self,
                                        pub_date=date_,
                                        raw=raw_)
        self.last_fetch = now()
        self.save()
