import random
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth import get_user_model

from base.choices import Coaches, JourneyStatus, BerthPreference, Gender

User = get_user_model()


class PassengerDetail(TimeStampedModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=15, choices=Gender.choices())
    quota = models.CharField(max_length=15, choices=Coaches.choices())
    berth_preference = models.CharField(
        max_length=15, choices=BerthPreference.choices(), null=True, blank=True)

    def __str__(self) -> str:
        return self.first_name

    class Meta:
        verbose_name = "Passenger Detail"
        verbose_name_plural = "Passenger Details"


class Ticket(TimeStampedModel):
    pnr = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(
        User, related_name="passenger", on_delete=models.CASCADE)
    passengers = models.ManyToManyField(
        PassengerDetail, related_name='passengers', through='Reservation')
    train = models.ForeignKey(
        'train.Train', related_name="train", on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(choices=JourneyStatus.choices(), max_length=15)
    source_station = models.ForeignKey(
        'train.City', related_name="source_station", on_delete=models.CASCADE)
    destination_station = models.ForeignKey(
        'train.City', related_name="destination_station", on_delete=models.CASCADE)
    boggy_number = models.CharField(max_length=50, null=True, blank=True)
    seat_number = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"


class Reservation(TimeStampedModel):
    passenger_detail = models.ForeignKey(
        PassengerDetail, on_delete=models.CASCADE)
    user_journey = models.ForeignKey(Ticket, on_delete=models.CASCADE)


class WaitingList(TimeStampedModel):
    user_journey = models.ManyToManyField(
        Ticket, through="WaitingDetailsUser")

    class Meta:
        verbose_name = "Waiting List"
        verbose_name_plural = "Waiting Lists"


class WaitingDetailsUser(models.Model):
    waiting_list = models.ForeignKey(WaitingList, on_delete=models.CASCADE)
    user_journey = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    waiting_number = models.IntegerField()


class ReservationChartForTrain(TimeStampedModel):
    user_journey = models.ManyToManyField(Ticket, blank=True)
    train = models.ForeignKey(
        'train.Train', related_name='reservation_charts', on_delete=models.CASCADE)
    total_seats = models.IntegerField(null=True, blank=True)
    vacant_seats = models.IntegerField(null=True, blank=True)
    waiting_list = models.ManyToManyField(WaitingList, blank=True)
    date = models.DateField()

    def __str__(self):
        return str(self.user_journey)

    class Meta:
        verbose_name = "Reservation Chart For Train"
        verbose_name_plural = "Reservation Chart For Trains"
        ordering = ['date']
