# Generated by Django 3.2 on 2022-10-04 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0011_userjourney_status1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userjourney',
            name='status1',
        ),
    ]
