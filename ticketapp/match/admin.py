from django.contrib import admin
from . import models


class MatchAdmin(admin.ModelAdmin):
    list_display = ('name', "series", "team1_name", "team1image_preview",
                    "team2_name", "team2image_preview", "start_time")
    readonly_fields = ('team1image_preview', "team2image_preview")

    def team1image_preview(self, obj):
        return obj.team1image_preview

    def team2image_preview(self, obj):
        return obj.team2image_preview


admin.site.register(models.Match, MatchAdmin)
