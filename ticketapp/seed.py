import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketapp.settings')

from seat.models import Seat
from row.models import Row



blocks = ['east', 'west', 'north', 'south']

for block in blocks:
   for i in [1, 2, 3, 4, 5, 6]:
       row = Row(name="row"+i+block)
       row.index = i
       row.save()
       for j in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
           seat = Seat(name="seat"+i+"row"+i+block)
           seat.row = row
           seat.index = j
           seat.save()
