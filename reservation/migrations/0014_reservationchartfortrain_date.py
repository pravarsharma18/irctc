# Generated by Django 3.2 on 2022-10-06 05:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0013_auto_20221004_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationchartfortrain',
            name='date',
            field=models.DateField(default=datetime.date(2022, 10, 6)),
            preserve_default=False,
        ),
    ]
