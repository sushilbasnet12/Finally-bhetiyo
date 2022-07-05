from django.template import Library
from django.core.serializers import serialize
register = Library()


@register.filter(name="gettotalpricefromreservation")
def gettotalpricefromreservation(queryset):
    total = 0
    for seatReservation in queryset:
        type = seatReservation.seat.type
        if(type == "VIP"):
            total = total + seatReservation.match.vipTicketPrice
        elif(type == "premium"):
            total = total + seatReservation.match.platinumTicketPrice
        else:
            total = total + seatReservation.match.normalTicketPrice
    return total
