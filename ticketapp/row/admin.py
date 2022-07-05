from django.contrib import admin

# Register your models here.
from . import models


class RowAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'block', 'index')


admin.site.register(models.Row, RowAdmin)
