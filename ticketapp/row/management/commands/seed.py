import os
from django.core.management.base import BaseCommand
from seat.models import Seat
from row.models import Row


class Command(BaseCommand):
    def handle(self, *args, **options):
       blocks = ['east', 'west', 'north', 'south']

       for block in blocks:
        for i in [1, 2, 3, 4, 5, 6]:
            row = Row(name="row"+str(i)+block, block=block, index=i)
            row.save()

            seats = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            if block == 'north' or block == 'south':
                seats = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 ,15, 16]

            for j in seats:

                seat = Seat(name="Seat "+str(j)+" Row " +
                            str(i) + " " + block.capitalize())
                seat.row = row

                seat.type = "normal"

                if row.index < 5:
                    seat.type = "VIP"

                if row.index < 3:
                    seat.type = "premium"

                seat.index = j
                seat.save()
