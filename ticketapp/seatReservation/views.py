from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SeatReservation
# Create your views here.
from django.db.models import Q
import datetime


@login_required(login_url="/auth/login")
def all(request):
    seatReservations = SeatReservation.objects.filter(
        user=request.user, expireDate__gte=datetime.datetime.now()).all()

    return render(request, 'reservations/index.html', context={
        'seatReservations': seatReservations
    })
