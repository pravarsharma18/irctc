from celery import shared_task
from datetime import datetime, timedelta

from base.choices import Constants, TotalSeats
from .models import ReservationChartForTrain
from train.models import Berth, Boggy, Train


@shared_task(name=f"Chart for next {Constants.BOOKING_FOR_NEXT_DAYS} days.")
def chart_for_next_BOOKING_FOR_NEXT_DAYS_days():
    train_qs = Train.objects.singles()
    for date in (datetime.now().date() + timedelta(days) for days in range(Constants.BOOKING_FOR_NEXT_DAYS+1)):
        reservation_qs = ReservationChartForTrain.objects.filter(
            train__in=train_qs, date=date)
        if not reservation_qs.exists():
            bulk_list = list()
            for train in train_qs:
                for days in train.runs_on:
                    if (days.title() == date.strftime('%A')):
                        res_objs = ReservationChartForTrain()
                        res_objs.train = train
                        res_objs.total_seats = Train.objects.get_total_seats(
                            train.number, date).get('total_seats', 0)
                        res_objs.vacant_seats = Train.objects.get_total_seats(
                            train.number, date).get('total_seats', 0)
                        res_objs.date = date
                        bulk_list.append(res_objs)
            ReservationChartForTrain.objects.bulk_create(bulk_list)
    print("ReservationChartForTrain objects created, total: ",
          ReservationChartForTrain.objects.all().count())


@shared_task(name=f"Chart Delete for Previous Day.")
def chart_delete_for_previous_days():

    ReservationChartForTrain.objects.filter(
        date=(datetime.now().date() - timedelta(days=1))).delete()

    print("ReservationChartForTrain objects created, total: ",
          ReservationChartForTrain.objects.all().count())


@shared_task(name=f"Create Boggy")
def create_boggy():
    for date in (datetime.now().date() + timedelta(days) for days in range(Constants.BOOKING_FOR_NEXT_DAYS)):
        reservation_qs = ReservationChartForTrain.objects.filter(date=date)
        if reservation_qs.exists():
            for res_obj in reservation_qs:
                if not Boggy.objects.filter(train=res_obj.train, date=date):
                    boggy_obj = Boggy()
                    boggy_obj.train = res_obj.train
                    boggy_obj.ac1 = TotalSeats.AC1.value
                    boggy_obj.ac2 = TotalSeats.AC2.value
                    boggy_obj.ac3 = TotalSeats.AC3.value
                    boggy_obj.sleeper = TotalSeats.SLEEPER.value
                    boggy_obj.date = date
                    boggy_obj.save()


@shared_task(name=f"Delete yesterday's Boggies and Berths")
def delete_boggy():
    Boggy.objects.filter(
        date=(datetime.now().date() - timedelta(days=1))).delete()
    Berth.objects.filter(
        date=(datetime.now().date() - timedelta(days=1))).delete()
