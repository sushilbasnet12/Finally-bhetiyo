from django.template import Library
from django.core.serializers import serialize
register = Library()


@register.filter(name="getrunningseries")
def getrunningseries(game):
    return game.serieses.filter(running=True).all()


