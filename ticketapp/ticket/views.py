from django.shortcuts import render
from .models import Ticket
# Create your views here.


def all(request):
    tickets = Ticket.objects.filter(
        user=request.user, valid=True).all()

    return render(request, 'tickets/index.html', context={
        'tickets': tickets
    })
