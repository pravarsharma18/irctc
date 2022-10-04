# Generated by Django 3.2 on 2022-09-26 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('train', '0004_alter_train_train_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserJourney',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('pnr', models.IntegerField()),
                ('status', models.CharField(choices=[('CONFIRMED', 'Confirmed'), ('WAITING', 'Waiting'), ('CANCELLED', 'Cancelled')], max_length=15)),
                ('boggy_number', models.CharField(blank=True, max_length=50, null=True)),
                ('seat_number', models.CharField(blank=True, max_length=50, null=True)),
                ('destination_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_station', to='train.city')),
                ('source_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_station', to='train.city')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='by_train', to='train.train')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passenger', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WaitingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('waiting_number', models.IntegerField()),
                ('user_journey', models.ManyToManyField(to='reservation.UserJourney')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReservationChartForTrain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('total_seats', models.IntegerField()),
                ('vacant_seats', models.IntegerField()),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train.train')),
                ('user_journey', models.ManyToManyField(to='reservation.UserJourney')),
                ('waiting_list', models.ManyToManyField(to='reservation.WaitingList')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
