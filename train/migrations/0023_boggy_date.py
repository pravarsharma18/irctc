# Generated by Django 3.2 on 2022-10-12 08:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0022_berth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='boggy',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
