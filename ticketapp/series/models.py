from django.db import models
from django.utils.html import mark_safe
from pathlib import Path

from game.models import Game
# Create your models here.
BASE_DIR = Path(__file__).parent.parent.resolve('resources')



class Series(models.Model):
    name = models.CharField(max_length=50)
    running = models.BooleanField(default=True)
    image = models.FileField(
        upload_to=BASE_DIR/"static/images/series", max_length=500)
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="serieses")

    def __str__(self):
        return self.name

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name_plural = 'Series'
