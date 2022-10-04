from django.db import models
from django_extensions.db.models import TimeStampedModel

from base.choices import Days, TrainType
from multiselectfield import MultiSelectField


class State(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ['name']


class City(TimeStampedModel):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, related_name="state", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = ['name']

class TrainQuerySet(models.QuerySet):

    def singles(self):
        return self.filter().distinct('train_number')

class TrainManager(models.Manager):

    def get_queryset(self):
        return TrainQuerySet(self.model, using=self._db)

    def singles(self):
        return self.get_queryset().singles()


class Train(TimeStampedModel):
    name = models.CharField(max_length=255)
    train_number = models.IntegerField(null=True, blank=True)
    station_code = models.CharField(max_length=10)
    station_name = models.CharField(max_length=255)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    source_station = models.CharField(max_length=255)
    source_short_name = models.CharField(max_length=10)
    destination_station = models.CharField(max_length=255)
    destination_short_name = models.CharField(max_length=10)
    sequence = models.IntegerField(null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=15, choices=TrainType.choices())
    runs_on = MultiSelectField(choices=Days.choices())

    objects = TrainManager()

    def __str__(self):
        return str(self.train_number)

    class Meta:
        verbose_name = "Train"
        verbose_name_plural = "Trains"
        ordering = ['train_number', 'sequence']
