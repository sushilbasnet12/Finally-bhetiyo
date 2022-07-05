import json
from channels.generic.websocket import WebsocketConsumer


from asgiref.sync import async_to_sync


class MatchConsumer(WebsocketConsumer):
    def connect(self):
        self.matchId = self.scope['url_route']['kwargs']['matchId']
        self.room_group_name = 'match_%s' % self.matchId
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print(self.room_group_name)
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def seat_reserved(self, event):
        print('test')
        self.send(text_data=json.dumps({
            'type': 'seat_reserved',
            'reservation': event['reservation']
        }))
    def seat_sold(self, event):
        print('test')
        self.send(text_data=json.dumps({
            'type': 'seat_sold',
            'reservation': event['reservation']
        }))