# Generated by Django 3.2 on 2021-04-23 17:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('last_fetch', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]