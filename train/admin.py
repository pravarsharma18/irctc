from django.contrib import admin

from .models import (State, City, Station, Train,
                     TrainWithStations, Boggy, Berth)


@admin.register(State)
class AdminState(admin.ModelAdmin):
    list_display = ['name', 'cities', 'city_count']

    @staticmethod
    def cities(obj):
        return [obj.name for obj in obj.state.all()]

    @staticmethod
    def city_count(obj):
        return obj.state.all().count()


@admin.register(City)
class AdminCity(admin.ModelAdmin):
    list_display = ['name', 'state']


@admin.register(Station)
class AdminStation(admin.ModelAdmin):
    list_display = ['id', 'name', 'city', 'short_name']


class AdminTrainWithStations(admin.TabularInline):
    model = TrainWithStations


@admin.register(Train)
class AdminTrain(admin.ModelAdmin):
    list_display = ['name', 'number']
    inlines = [
        AdminTrainWithStations,
    ]


# @admin.register(TrainWithStations)
# class AdminTrainWithStations(admin.ModelAdmin):
#     list_display = ['station', 'train', 'sequence', 'distance']


@admin.register(Boggy)
class AdminBoggy(admin.ModelAdmin):
    list_display = ['train', 'date']


@admin.register(Berth)
class AdminBerth(admin.ModelAdmin):
    list_display = ['train', 'name', 'date']
    list_filter = ('train', 'date')
