import enum
from django.db import models

# Create your models here.


class Row(models.Model):
    class Block(enum.Enum):
        EAST = "east"
        WEST = "west"
        NORTH = "north"
        SOUTH = "south"
    name = models.CharField(max_length=30)
    index = models.IntegerField()
    block = models.CharField(
        choices=[(choice.value, choice.name) for choice in Block], max_length=30)

    class Meta:
        unique_together = ("block", "index")

    def __str__(self):
        return self.name
