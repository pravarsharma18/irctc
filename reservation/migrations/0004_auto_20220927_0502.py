# Generated by Django 3.2 on 2022-09-27 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_auto_20220927_0459'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='passengerdetail',
            options={'verbose_name': 'Passenger Detail', 'verbose_name_plural': 'Passenger Details'},
        ),
        migrations.AlterModelOptions(
            name='reservationchartfortrain',
            options={'verbose_name': 'Reservation Chart For Train', 'verbose_name_plural': 'Reservation Chart For Trains'},
        ),
        migrations.AlterModelOptions(
            name='userjourney',
            options={'verbose_name': 'User Journey', 'verbose_name_plural': 'User Journeys'},
        ),
        migrations.AlterModelOptions(
            name='waitinglist',
            options={'verbose_name': 'Waiting List', 'verbose_name_plural': 'Waiting Lists'},
        ),
    ]
