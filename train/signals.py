from django.db.models.signals import post_save
from django.dispatch import receiver

from base.choices import BoggyName

from base.choices import PassengerSeats
from reservation.models import ReservationChartForTrain
from .models import Boggy, Berth, Train
# Signal to Create Bert of all the Boggies of a Train on a Particular Day.


@ receiver(post_save, sender=Boggy)
def create_berths(sender, instance, **kwargs):
    ac1_bulk_list = []
    ac2_bulk_list = []
    ac3_bulk_list = []
    sleeper_bulk_list = []
    for index in range(1, instance.ac1+1):
        berth_obj = Berth.objects.filter(
            train=instance.train, name=f"{BoggyName.AC1.value}-{index}", date=instance.date)
        if not berth_obj:
            data = {
                'train': instance.train,
                'name': f"{BoggyName.AC1.value}-{index}",
                'lower': PassengerSeats.AC1_LOWER.value,
                'upper': PassengerSeats.AC1_UPPER.value,
                'date': instance.date
            }
            ac1_bulk_list.append(Berth(**data))
    Berth.objects.bulk_create(ac1_bulk_list)
    for index in range(1, instance.ac2+1):
        berth_obj = Berth.objects.filter(
            train=instance.train, name=f"{BoggyName.AC2.value}-{index}", date=instance.date)
        if not berth_obj:
            data = {
                'train': instance.train,
                'name': f"{BoggyName.AC1.value}-{index}",
                'lower': PassengerSeats.AC1_LOWER.value,
                'upper': PassengerSeats.AC1_UPPER.value,
                'side_upper': PassengerSeats.AC2_SIDE_UPPER.value,
                'side_lower': PassengerSeats.AC2_SIDE_LOWER.value,
                'date': instance.date
            }
            ac2_bulk_list.append(Berth(**data))
    Berth.objects.bulk_create(ac2_bulk_list)
    for index in range(1, instance.ac3+1):
        berth_obj = Berth.objects.filter(
            train=instance.train, name=f"{BoggyName.AC3.value}-{index}", date=instance.date)
        if not berth_obj:
            data = {
                'train': instance.train,
                'name': f"{BoggyName.AC3.value}-{index}",
                'lower': PassengerSeats.AC3_LOWER.value,
                'middle': PassengerSeats.AC3_MIDDLE.value,
                'upper': PassengerSeats.AC3_UPPER.value,
                'side_upper': PassengerSeats.AC3_SIDE_UPPER.value,
                'side_lower': PassengerSeats.AC3_SIDE_LOWER.value,
                'date': instance.date
            }
            ac3_bulk_list.append(Berth(**data))
    Berth.objects.bulk_create(ac3_bulk_list)
    for index in range(1, instance.sleeper+1):
        berth_obj = Berth.objects.filter(
            train=instance.train, name=f"{BoggyName.SLEEPER.value}-{index}", date=instance.date)
        if not berth_obj:
            data = {
                'train': instance.train,
                'name': f"{BoggyName.SLEEPER.value}-{index}",
                'lower': PassengerSeats.SLEEPER_LOWER.value,
                'middle': PassengerSeats.SLEEPER_MIDDLE.value,
                'upper': PassengerSeats.SLEEPER_UPPER.value,
                'side_upper': PassengerSeats.SLEEPER_SIDE_UPPER.value,
                'side_lower': PassengerSeats.SLEEPER_SIDE_LOWER.value,
                'date': instance.date
            }
            sleeper_bulk_list.append(Berth(**data))
    Berth.objects.bulk_create(sleeper_bulk_list)

    # Update the total seats in ReservationChartForTrain model accordingly
    reservation_qs = ReservationChartForTrain.objects.filter(
        train=instance.train, date=instance.date)
    if reservation_qs.exists():
        reservation_obj = reservation_qs.first()

        total_seats = Train.objects.get_total_seats(
            instance.train.number, instance.date).get('total_seats', 0)
        # to update the new vacant seats
        new_seats = total_seats - reservation_obj.total_seats

        reservation_obj.total_seats = total_seats
        reservation_obj.vacant_seats += new_seats
        reservation_obj.save()
