# Generated by Django 3.2 on 2022-10-14 07:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0025_auto_20221013_0839'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0023_auto_20221014_0615'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserJourney',
            new_name='Ticket',
        ),
    ]
