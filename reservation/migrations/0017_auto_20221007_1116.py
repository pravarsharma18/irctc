# Generated by Django 3.2 on 2022-10-07 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0016_auto_20221007_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitingDetailsUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waiting_number', models.IntegerField()),
                ('user_journey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.userjourney')),
                ('waiting_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.waitinglist')),
            ],
        ),
        migrations.AddField(
            model_name='waitinglist',
            name='user_journey',
            field=models.ManyToManyField(through='reservation.WaitingDetailsUser', to='reservation.UserJourney'),
        ),
    ]