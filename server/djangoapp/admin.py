from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
