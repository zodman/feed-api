"""
Script for populate the default admin, used on docker-compose.yaml

"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
import django

django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin")
