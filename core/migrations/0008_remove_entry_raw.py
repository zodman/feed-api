# Generated by Django 3.2 on 2021-04-27 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_entry_raw'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='raw',
        ),
    ]