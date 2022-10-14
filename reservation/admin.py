from django.contrib import admin

from .models import Reservation, Ticket, WaitingList, ReservationChartForTrain, PassengerDetail, WaitingDetailsUser
# Register your models here.


@admin.register(PassengerDetail)
class AdminPassengerDetail(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'age', 'berth_preference']


class AdminReservation(admin.TabularInline):
    # list_display = ['first_name', 'last_name', 'age', 'birth_preference']
    model = Reservation
    # extra = 1


@admin.register(Ticket)
class AdminUserJourney(admin.ModelAdmin):
    list_display = ['pnr', 'user']
    list_select_related = ('train',)
    inlines = [
        AdminReservation,
    ]


class AdminWaitingDetailsUser(admin.TabularInline):
    # list_display = ['waiting_list', 'user_journey', 'waiting_number']
    model = WaitingDetailsUser
    # extra = 1


@admin.register(WaitingList)
class AdminWaitingList(admin.ModelAdmin):
    # list_display = ['user_journey']

    inlines = [
        AdminWaitingDetailsUser,
    ]

    # def user_journey(self, obj):
    #     return "\n".join([a.user.first_name for a in obj.user_journey_set.all()])


@admin.register(ReservationChartForTrain)
class AdminReservationChartForTrain(admin.ModelAdmin):
    list_display = ['train', 'total_seats', 'vacant_seats', 'date']
    list_select_related = ('train',)
