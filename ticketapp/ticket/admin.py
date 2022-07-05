from django.contrib import admin

# Register your models here.
from . import models


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', "match", "user", "seat")
    search_fields = ['id']


admin.site.register(models.Ticket, TicketAdmin)
