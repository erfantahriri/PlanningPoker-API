from channels.generic.websocket import AsyncWebsocketConsumer
import json


class RoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_uid = self.scope['url_route']['kwargs']['room_uid']
        self.room_group_name = 'room_{room_uid}'.format(room_uid=self.room_uid)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'current_issue',
                'content': message['content']
            }
        )

    async def current_issue(self, message):

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    async def add_issue(self, message):

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    async def add_participant(self, message):

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    async def add_vote(self, message):

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    async def update_issue(self, message):

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
