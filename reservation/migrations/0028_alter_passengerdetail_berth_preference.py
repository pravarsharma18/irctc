# Generated by Django 3.2 on 2022-10-15 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0027_auto_20221014_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passengerdetail',
            name='berth_preference',
            field=models.CharField(blank=True, choices=[('LOWER', 'Lower Berth'), ('MIDDLE', 'Middle Berth'), ('UPPER', 'Upper Berth'), ('SIDE_LOWER', 'Side Lower Berth'), ('SIDE_UPPER', 'Side Upper Berth')], max_length=15, null=True),
        ),
    ]
