from django.db import models

from match.models import Match
from user.models import NewUser

from seat.models import Seat
# Create your models here.


class SeatReservation(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    expireDate = models.DateTimeField(
        auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.user.id)
