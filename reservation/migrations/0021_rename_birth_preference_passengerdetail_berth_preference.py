# Generated by Django 3.2 on 2022-10-13 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0020_passengerdetail_quota'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passengerdetail',
            old_name='birth_preference',
            new_name='berth_preference',
        ),
    ]
