import random
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver

from train.models import Train, City
from base.choices import JourneyStatus, BirthPreference, Gender

User = get_user_model()


class PassengerDetail(TimeStampedModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=15, choices=Gender.choices())
    birth_preference = models.CharField(max_length=15, choices=BirthPreference.choices(), null=True, blank=True)

    def __str__(self) -> str:
        return self.first_name

    class Meta:
        verbose_name = "Passenger Detail"
        verbose_name_plural = "Passenger Details"


class UserJourney(TimeStampedModel):
    pnr = models.IntegerField()
    user = models.ForeignKey(User, related_name="passenger", on_delete=models.CASCADE)
    passengers = models.ManyToManyField(PassengerDetail, related_name='passengers', through='Reservation')
    train = models.ForeignKey(Train, related_name="train", on_delete=models.CASCADE)
    status = models.CharField(choices=JourneyStatus.choices(), max_length=15)
    source_station = models.ForeignKey(City, related_name="source_station", on_delete=models.CASCADE)
    destination_station = models.ForeignKey(City, related_name="destination_station", on_delete=models.CASCADE)
    boggy_number = models.CharField(max_length=50, null=True, blank=True)
    seat_number = models.CharField(max_length=50, null=True, blank=True)


    class Meta:
        verbose_name = "User Journey"
        verbose_name_plural = "User Journeys"


class Reservation(TimeStampedModel):
    passenger_detail = models.ForeignKey(PassengerDetail, on_delete=models.CASCADE)
    user_journey = models.ForeignKey(UserJourney, on_delete=models.CASCADE)



@receiver(pre_save, sender=UserJourney)
def my_callback(sender, instance, *args, **kwargs):
    if not instance.pnr:
        instance.pnr = random.randint(10000000,100000000)


class WaitingList(TimeStampedModel):
    user_journey = models.ManyToManyField(UserJourney)
    waiting_number = models.IntegerField()

    def __str__(self):
        return self.user_journey.user.first_name

    class Meta:
        verbose_name = "Waiting List"
        verbose_name_plural = "Waiting Lists"


class ReservationChartForTrain(TimeStampedModel):
    user_journey = models.ManyToManyField(UserJourney, blank=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    total_seats = models.IntegerField()
    vacant_seats = models.IntegerField()
    waiting_list = models.ManyToManyField(WaitingList, blank=True)

    def __str__(self):
        return str(self.user_journey)#.user.first_name

    class Meta:
        verbose_name = "Reservation Chart For Train"
        verbose_name_plural = "Reservation Chart For Trains"
