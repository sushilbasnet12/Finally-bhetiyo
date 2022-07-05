import enum
from django.db import models

from row.models import Row

# Create your models here.


class Seat(models.Model):
    class SeatType(enum.Enum):
        NORMAL = "normal"
        PREMIUM = "premium"
        VIP = "VIP"

    name = models.CharField(max_length=30)
    row = models.ForeignKey(Row, on_delete=models.CASCADE)
    index = models.IntegerField()
    type = models.CharField(
        choices=[(choice.value, choice.name) for choice in SeatType], max_length=30
    )

    class Meta:
        unique_together = ("row", "index")

    def __str__(self):
        return self.name
