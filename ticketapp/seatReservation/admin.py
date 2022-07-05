from django.contrib import admin

# Register your models here.
from . import models


class SeatReservationAdmin(admin.ModelAdmin):
    list_displat = ("match", "user", "seat")


admin.site.register(models.SeatReservation, SeatReservationAdmin)
