# Generated by Django 3.2 on 2022-10-03 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0008_alter_passengerdetail_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passengerdetail',
            name='birth_preference',
            field=models.CharField(blank=True, choices=[('LOWER', 'Lower'), ('MIDDLE', 'Middle'), ('UPPER', 'Upper'), ('SIDEUPPER', 'Sideupper')], max_length=15, null=True),
        ),
    ]
