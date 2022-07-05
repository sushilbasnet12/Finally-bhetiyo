from django.contrib import admin

# Register your models here.
from . import models


class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'thumbnail_preview')

    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True


admin.site.register(models.Game, GameAdmin)
