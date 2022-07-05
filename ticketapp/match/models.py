from pathlib import Path
from django.db import models
from django.utils.html import mark_safe

from game.models import Game
from series.models import Series
BASE_DIR = Path(__file__).parent.parent.resolve('resources')



class Match(models.Model):
    name = models.CharField(max_length=50)
    team1_name = models.CharField(max_length=50)
    team2_name = models.CharField(max_length=50)
    team1_image = models.FileField(
        upload_to=BASE_DIR/"static/images/teams", max_length=500)
    team2_image = models.FileField(
        upload_to=BASE_DIR/"static/images/teams", max_length=500)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    normalTicketPrice = models.IntegerField(default=200)
    platinumTicketPrice = models.IntegerField(default=500)
    vipTicketPrice = models.IntegerField(default=1000)
    ticket_reserve_open = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name

    @property
    def team1image_preview(self):
        if self.team1_image:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(self.team1_image.url))
        return ""

    @property
    def team2image_preview(self):
        if self.team2_image:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(self.team2_image.url))
        return ""

    class Meta:
        verbose_name_plural = 'Matches'
