# Generated by Django 3.2 on 2022-10-06 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0012_alter_train_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='train',
            options={'ordering': ['number'], 'verbose_name': 'Train', 'verbose_name_plural': 'Trains'},
        ),
        migrations.RenameField(
            model_name='train',
            old_name='distance',
            new_name='number',
        ),
        migrations.RemoveField(
            model_name='train',
            name='arrival_time',
        ),
        migrations.RemoveField(
            model_name='train',
            name='departure_time',
        ),
        migrations.RemoveField(
            model_name='train',
            name='destination_short_name',
        ),
        migrations.RemoveField(
            model_name='train',
            name='destination_station',
        ),
        migrations.RemoveField(
            model_name='train',
            name='sequence',
        ),
        migrations.RemoveField(
            model_name='train',
            name='source_short_name',
        ),
        migrations.RemoveField(
            model_name='train',
            name='source_station',
        ),
        migrations.RemoveField(
            model_name='train',
            name='station_code',
        ),
        migrations.RemoveField(
            model_name='train',
            name='station_name',
        ),
        migrations.RemoveField(
            model_name='train',
            name='train_number',
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city', to='train.city')),
            ],
        ),
    ]
