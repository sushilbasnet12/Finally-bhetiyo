"""ticketapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import datetime
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.shortcuts import redirect, render
from django.views import View
import requests
from game.models import Game
from seatReservation.models import SeatReservation
from ticket.models import Ticket
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from django.forms.models import model_to_dict

def home(request):

    return render(request, 'index.html', {})


def about(request):
    return render(request, 'about/about.html')


def contact(request):
    return render(request, 'contact/contact.html')


def register(request):
    return render(request, 'register.html', {})


def defaultconverter(o):
  if isinstance(o, datetime.datetime):
      return o.__str__()


class KhaltiVerifyView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        amount = request.GET.get("amount")
        print(token, amount, )

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": "Key test_secret_key_f59e8b7d18b4499ca40f68195a846e9b"
        }
        seatReservations = SeatReservation.objects.filter(
            user=request.user, expireDate__gte=datetime.datetime.now()).all()

        total = 0
        for seatReservation in seatReservations:
            type = seatReservation.seat.type
            if(type == "VIP"):
                total = total + seatReservation.match.vipTicketPrice
            elif(type == "premium"):
                total = total + seatReservation.match.platinumTicketPrice
            else:
                total = total + seatReservation.match.normalTicketPrice
        if int(total*100) == int(amount):
            response = requests.post(url, payload, headers=headers)
            resp_dict = response.json()
            print()
            tickets = []
            if resp_dict.get("idx"):
                for seatReservation in seatReservations:
                    ticket = Ticket(seat=seatReservation.seat,
                                    user=seatReservation.user, match=seatReservation.match)
                    ticket.save()
                    tickets.append(ticket)
                    layer = get_channel_layer()
                    async_to_sync(layer.group_send)('match_'+str(seatReservation.match.id), {
                        'type': 'seat_sold',
                        'reservation': json.loads(json.dumps(model_to_dict(ticket), default=defaultconverter))
                    })
                seatReservations.delete()
                success = True

                current_site = get_current_site(request)
                mail_subject = 'Ticket Receipt'
                message = render_to_string('receipt_template.html', {
                    'user': request.user,
                    'domain': current_site.domain,
                    'token': token,
                    'amount': int(amount) / 100,
                    'tickets': tickets,
                    'paid_by': resp_dict['user']['name']

                })
                to_email = request.user.email
                send_mail('Ticket Bought Successfully', mail_subject,
                          None, [to_email],  html_message=message)
            else:
                success = False
        else:
            success = False
        data = {
            "success": success
        }

        return JsonResponse(data)


urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name="contact"),
    path('khalti-verify/', KhaltiVerifyView.as_view()),
    path('matches/', include('match.urls'), name="tickets"),
    path('auth/', include('user.urls')),
    path('reservations/', include('seatReservation.urls')),
    path('tickets/', include('ticket.urls')),
    path('admin/', admin.site.urls),
]
