# Generated by Django 3.2 on 2022-10-12 07:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0021_auto_20221012_0641'),
    ]

    operations = [
        migrations.AddField(
            model_name='berth',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
