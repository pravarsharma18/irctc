# Generated by Django 3.2 on 2022-10-12 06:25

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0018_auto_20221010_0504'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trainwithstations',
            options={'ordering': ['train__number', 'sequence']},
        ),
        migrations.CreateModel(
            name='Boogy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('ac1', models.IntegerField()),
                ('ac2', models.IntegerField()),
                ('ac3', models.IntegerField()),
                ('sleeper', models.IntegerField()),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train.train')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
