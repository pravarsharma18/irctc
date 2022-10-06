from celery import shared_task
from datetime import datetime, timedelta

from base.choices import Constants
from .models import ReservationChartForTrain
from train.models import Train

@shared_task(name=f"Chart for next {Constants.BOOKING_FOR_NEXT_DAYS} days.")
def chart_for_next_BOOKING_FOR_NEXT_DAYS_days():
    train_qs = Train.objects.singles()
    for date in (datetime.now().date() + timedelta(days) for days in range(Constants.BOOKING_FOR_NEXT_DAYS)):
        reservation_qs = ReservationChartForTrain.objects.filter(date=date)
        if not reservation_qs.exists():
            bulk_list = []
            for train in train_qs:
                res_objs = ReservationChartForTrain()
                res_objs.train = train
                res_objs.total_seats = Constants.TOTAL_SEATS
                res_objs.vacant_seats = Constants.TOTAL_SEATS
                res_objs.date = date
                bulk_list.append(res_objs)
            ReservationChartForTrain.objects.bulk_create(bulk_list)
    print("ReservationChartForTrain objects created, total: ", ReservationChartForTrain.objects.all().count())


@shared_task(name=f"Chart Delete for Previous Day.")
def chart_delete_for_previous_days():
    
    ReservationChartForTrain.objects.filter(date = (datetime.now().date() - timedelta(days=1))).delete()

    print("ReservationChartForTrain objects created, total: ", ReservationChartForTrain.objects.all().count())
