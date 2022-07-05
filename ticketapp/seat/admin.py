from django.contrib import admin

# Register your models here.
from . import models


class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',  'row', 'type')


admin.site.register(models.Seat, SeatAdmin)
