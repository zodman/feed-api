from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
    path("", lambda x: redirect("/api/feed/")),
]
