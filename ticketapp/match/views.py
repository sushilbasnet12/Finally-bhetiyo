import json

from ticket.models import Ticket
from .models import Match
import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect, render
from row.models import Row
from seat.models import Seat
from seatReservation.models import SeatReservation
from django.shortcuts import redirect, render
now = datetime.datetime.now()


def index(request):
    matches = Match.objects.filter(ticket_reserve_open=True).all()
    layer = get_channel_layer()

    print(matches)
    return render(request, 'match/index.html', context={
        'matches': matches
    })


@login_required(login_url="/auth/login")
def match(request, id):
    print(id)
    matches = Match.objects.filter(id=id).all()
    seats = Seat.objects.all()
    rows = Row.objects.all()
    seatReservations = SeatReservation.objects.filter(
        match__id=id, expireDate__gte=datetime.datetime.now()).all()
    tickets = Ticket.objects.filter(
        match_id=id
    )
    print(match)
    return render(request, 'match/match.html', context={
        'matches': matches,
        'seats': seats,
        'rows': rows,
        'seatReservations': seatReservations,
        'tickets': tickets
    })


def defaultconverter(o):
  if isinstance(o, datetime.datetime):
      return o.__str__()


@login_required(login_url="/auth/login")
def reserve(request, id):
    seatsString = request.POST.get('seats').split(",")

    seats = [int(seat) for seat in seatsString]
    seatReservations = list(SeatReservation.objects.filter(
        match__id=id, seat__id__in=seats, expireDate__gte=datetime.datetime.now()).values())
    if len(seatReservations) == 0:
        for seat in seats:
            reservation = SeatReservation(
                match=Match.objects.get(pk=id), seat=Seat.objects.get(pk=seat), user=request.user, expireDate=datetime.datetime.now()+datetime.timedelta(days=1))
            reservation.save()
            layer = get_channel_layer()
            async_to_sync(layer.group_send)('match_'+str(id), {
                'type': 'seat_reserved',
                'reservation': json.loads(json.dumps(model_to_dict(reservation), default=defaultconverter))
            })

    return redirect("reservations")
