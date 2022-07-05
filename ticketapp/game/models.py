
# Create your models here.
from django.db import models
from pathlib import Path
# Create your models here.
# Register your models here.
from django.utils.html import mark_safe


BASE_DIR = Path(__file__).parent.parent.resolve('resources')


class Game(models.Model):
    name = models.CharField(max_length=30)
    image = models.FileField(upload_to=BASE_DIR /
                             "static/images/games", max_length=500, )

    def __str__(self):
        return self.name

    @property
    def thumbnail_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(self.image.url))
        return ""
