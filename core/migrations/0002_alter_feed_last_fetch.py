# Generated by Django 3.2 on 2021-04-23 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="feed",
            name="last_fetch",
            field=models.DateTimeField(blank=True, null=True),
        )
    ]
