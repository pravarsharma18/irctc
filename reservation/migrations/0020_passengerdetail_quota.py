# Generated by Django 3.2 on 2022-10-13 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0019_alter_reservationchartfortrain_train'),
    ]

    operations = [
        migrations.AddField(
            model_name='passengerdetail',
            name='quota',
            field=models.CharField(choices=[('AC1', 'First AC'), ('AC2', 'Second AC'), ('AC3', 'Third AC'), ('SLEEPER', 'Sleeper')], default='AC1', max_length=15),
            preserve_default=False,
        ),
    ]
