from .models import Game

from match.models import Match


def games(request):
    games = Game.objects.all()
    return {
        'games': games,
    }
