from channels.generic.websocket import AsyncWebsocketConsumer
import json


class RoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_uid = self.scope['url_route']['kwargs']['room_uid']
        self.room_group_name = 'room_{}'.format(self.room_uid)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'current_issue', 'content': message['content']}
        )

    async def _forward_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def current_issue(self, message):
        await self._forward_message(message)

    async def add_issue(self, message):
        await self._forward_message(message)

    async def add_participant(self, message):
        await self._forward_message(message)

    async def add_vote(self, message):
        await self._forward_message(message)

    async def update_issue(self, message):
        await self._forward_message(message)
