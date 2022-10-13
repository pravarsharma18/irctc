from django.db import models
from django_extensions.db.models import TimeStampedModel

from base.choices import Days, PassengerSeats, TrainType, TotalSeats
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime
from base.choices import BoggyName

from reservation.models import ReservationChartForTrain


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

    def get_total_seats(self):
        return self.get_queryset().filter()


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
    arrival = models.TimeField()
    departure = models.TimeField()

    class Meta:
        ordering = ['train__number', 'sequence']


class BoggyQuerySet(models.QuerySet):
    def get_seats(self):
        return self

    # def editors(self):
    #     return self.filter(role='E')


class BoggyManager(models.Manager):
    def get_queryset(self):
        return BoggyQuerySet(self.model, using=self._db)

    def total_seats(self, train_number, date):
        return self.get_queryset().filter(train__number=train_number, date=date)


class Boggy(TimeStampedModel):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    ac1 = models.IntegerField()
    ac2 = models.IntegerField()
    ac3 = models.IntegerField()
    sleeper = models.IntegerField()
    date = models.DateField()

    objects = BoggyManager()

    def __str__(self) -> str:
        return self.train.name


class Berth(TimeStampedModel):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    lower = models.IntegerField(null=True, blank=True)
    middle = models.IntegerField(null=True, blank=True)
    upper = models.IntegerField(null=True, blank=True)
    side_upper = models.IntegerField(null=True, blank=True)
    side_lower = models.IntegerField(null=True, blank=True)
    date = models.DateField()

    def __str__(self) -> str:
        return self.name


# Signal to Create Bert of all the Boggies of a Train on a Particular Day.
@receiver(post_save, sender=Boggy)
def update_stock(sender, instance, **kwargs):
    reservation_chart = ReservationChartForTrain.objects.filter(
        train=instance.train)
    if reservation_chart.exists():
        for res_obj in reservation_chart:
            for index in range(1, instance.ac1+1):
                berth_obj = Berth.objects.filter(
                    train=instance.train, name=f"{BoggyName.AC1.value}-{index}", date=res_obj.date)
                if not berth_obj:
                    berth_obj = Berth()
                    berth_obj.train = instance.train
                    berth_obj.name = f"{BoggyName.AC1.value}-{index}"
                    berth_obj.lower = PassengerSeats.AC1_LOWER.value
                    berth_obj.upper = PassengerSeats.AC1_UPPER.value
                    berth_obj.date = res_obj.date
                    berth_obj.save()
            for index in range(1, instance.ac2+1):
                berth_obj = Berth.objects.filter(
                    train=instance.train, name=f"{BoggyName.AC2.value}-{index}", date=res_obj.date)
                if not berth_obj:
                    berth_obj = Berth()
                    berth_obj.train = instance.train
                    berth_obj.name = f"{BoggyName.AC2.value}-{index}"
                    berth_obj.lower = PassengerSeats.AC2_LOWER.value
                    berth_obj.upper = PassengerSeats.AC2_UPPER.value
                    berth_obj.side_upper = PassengerSeats.AC2_SIDE_UPPER.value
                    berth_obj.side_lower = PassengerSeats.AC2_SIDE_LOWER.value
                    berth_obj.date = res_obj.date
                    berth_obj.save()
            for index in range(1, instance.ac3+1):
                berth_obj = Berth.objects.filter(
                    train=instance.train, name=f"{BoggyName.AC3.value}-{index}", date=res_obj.date)
                if not berth_obj:
                    berth_obj = Berth()
                    berth_obj.train = instance.train
                    berth_obj.name = f"{BoggyName.AC3.value}-{index}"
                    berth_obj.lower = PassengerSeats.AC3_LOWER.value
                    berth_obj.middle = PassengerSeats.AC3_MIDDLE.value
                    berth_obj.upper = PassengerSeats.AC3_UPPER.value
                    berth_obj.side_upper = PassengerSeats.AC3_SIDE_UPPER.value
                    berth_obj.side_lower = PassengerSeats.AC3_SIDE_LOWER.value
                    berth_obj.date = res_obj.date
                    berth_obj.save()
            for index in range(1, instance.sleeper+1):
                berth_obj = Berth.objects.filter(
                    train=instance.train, name=f"{BoggyName.SLEEPER.value}-{index}", date=res_obj.date)
                if not berth_obj:
                    berth_obj = Berth()
                    berth_obj.train = instance.train
                    berth_obj.name = f"{BoggyName.SLEEPER.value}-{index}"
                    berth_obj.lower = PassengerSeats.SLEEPER_LOWER.value
                    berth_obj.middle = PassengerSeats.SLEEPER_MIDDLE.value
                    berth_obj.upper = PassengerSeats.SLEEPER_UPPER.value
                    berth_obj.side_upper = PassengerSeats.SLEEPER_SIDE_UPPER.value
                    berth_obj.side_lower = PassengerSeats.SLEEPER_SIDE_LOWER.value
                    berth_obj.date = res_obj.date
                    berth_obj.save()
