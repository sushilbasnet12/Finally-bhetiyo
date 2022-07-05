from django.contrib import admin

# Register your models here.
from . import models


class SeriesAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview")

    def image_preview(self, obj):
        return obj.image_preview


admin.site.register(models.Series, SeriesAdmin)
