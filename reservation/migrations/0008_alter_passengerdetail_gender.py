# Generated by Django 3.2 on 2022-10-03 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_passengerdetail_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passengerdetail',
            name='gender',
            field=models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHERs', 'Others')], max_length=15),
        ),
    ]
