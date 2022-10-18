from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.db.models import Sum

from base.choices import Days, PassengerSeats, TrainType, TotalSeats
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

    def get_total_seats(self, number, date):
        final_sum = (Sum('ac1')*(PassengerSeats.AC1_LOWER.value+PassengerSeats.AC2_UPPER.value)) \
            + (Sum('ac2')*(PassengerSeats.AC2_LOWER.value+PassengerSeats.AC2_UPPER.value +
                           PassengerSeats.AC2_SIDE_UPPER.value + PassengerSeats.AC2_SIDE_LOWER.value))  \
            + (Sum('ac3')*(PassengerSeats.AC3_LOWER.value+PassengerSeats.AC3_UPPER.value +
                           PassengerSeats.AC3_MIDDLE.value + PassengerSeats.AC3_SIDE_UPPER.value +
                           PassengerSeats.AC3_SIDE_LOWER.value)) \
            + (Sum('ac3')*(PassengerSeats.AC3_LOWER.value+PassengerSeats.AC3_UPPER.value +
                           PassengerSeats.AC3_MIDDLE.value + PassengerSeats.AC3_SIDE_UPPER.value +
                           PassengerSeats.AC3_SIDE_LOWER.value)) \
            + (Sum('sleeper')*(PassengerSeats.SLEEPER_LOWER.value+PassengerSeats.SLEEPER_MIDDLE.value +
                               PassengerSeats.SLEEPER_UPPER.value + PassengerSeats.SLEEPER_SIDE_UPPER.value +
                               PassengerSeats.SLEEPER_SIDE_LOWER.value))
        return Boggy.objects.total_seats(number, date).aggregate(total_seats=final_sum)


class TrainManager(models.Manager):

    def get_queryset(self):
        return TrainQuerySet(self.model, using=self._db)

    def singles(self):
        return self.get_queryset().singles()

    def get_total_seats(self, number, date):
        return self.get_queryset().get_total_seats(number, date)


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

    class Meta:
        verbose_name = "Boggy"
        verbose_name_plural = "Boggies"
        ordering = ['-date']


class Berth(TimeStampedModel):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=50)
    lower = models.IntegerField(null=True, blank=True)
    middle = models.IntegerField(null=True, blank=True)
    upper = models.IntegerField(null=True, blank=True)
    side_upper = models.IntegerField(null=True, blank=True)
    side_lower = models.IntegerField(null=True, blank=True)
    date = models.DateField(db_index=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        # indexes = [
        #     ['name']
        # ]
        verbose_name = "Berth"
        verbose_name_plural = "Berths"
        ordering = ['-date']
