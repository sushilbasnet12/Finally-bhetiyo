from django.db import models
from match.models import Match
from user.models import NewUser
from seat.models import Seat
# Create your models here.


class Ticket(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    valid = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)
