from django.contrib import admin

from .models import State, City, Train


@admin.register(State)
class AdminState(admin.ModelAdmin):
    list_display = ['name','cities', 'city_count']

    @staticmethod
    def cities(obj):
        return [obj.name for obj in obj.state.all()]

    @staticmethod
    def city_count(obj):
        return obj.state.all().count()


@admin.register(City)
class AdminCity(admin.ModelAdmin):
    list_display = ['name', 'state']


@admin.register(Train)
class AdminTrain(admin.ModelAdmin):
    list_display = ['name', 'train_number', 'sequence']
