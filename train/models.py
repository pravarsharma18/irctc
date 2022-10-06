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
    state = models.ForeignKey(
        State, related_name="state", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = ['name']


class Station(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, related_name='city',
                             on_delete=models.CASCADE)
    short_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Station"
        verbose_name_plural = "Stations"


class TrainQuerySet(models.QuerySet):

    def singles(self):
        return self.filter().distinct('number')


class TrainManager(models.Manager):

    def get_queryset(self):
        return TrainQuerySet(self.model, using=self._db)

    def singles(self):
        return self.get_queryset().singles()


class Train(TimeStampedModel):
    name = models.CharField(max_length=255)
    number = models.IntegerField(null=True, blank=True)
    station = models.ManyToManyField(
        Station, related_name="stations", through='TrainWithStations')
    type = models.CharField(max_length=15, choices=TrainType.choices())
    runs_on = MultiSelectField(choices=Days.choices())

    objects = TrainManager()

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = "Train"
        verbose_name_plural = "Trains"
        ordering = ['number']


class TrainWithStations(TimeStampedModel):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    sequence = models.IntegerField()
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    base_fare = models.DecimalField(max_digits=5, decimal_places=2)
