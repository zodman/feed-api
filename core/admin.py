from django.contrib import admin
from .models import Feed, Follow, ReadedEntry


admin.site.register(Feed)
admin.site.register(ReadedEntry)
admin.site.register(Follow)
