from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime, timezone
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
        msg_type = message.get('type')

        if msg_type == 'chat_message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'content': {
                        'sender': message['content']['sender'],
                        'senderUid': message['content'].get('senderUid'),
                        'text': message['content']['text'],
                        'timestamp': datetime.now(timezone.utc).isoformat(),
                    },
                }
            )
        elif msg_type == 'timer_start':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'timer_start',
                    'content': {
                        'duration': message['content']['duration'],
                        'started_at': datetime.now(timezone.utc).isoformat(),
                    },
                }
            )
        elif msg_type == 'timer_stop':
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'timer_stop', 'content': {}}
            )
        elif msg_type == 'reaction':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'reaction',
                    'content': {
                        'participantName': message['content'].get('participantName', ''),
                        'emoji': message['content']['emoji'],
                        'id': datetime.now(timezone.utc).isoformat() + message['content'].get('participantName', ''),
                    },
                }
            )
        else:
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

    async def rename_participant(self, message):
        await self._forward_message(message)

    async def update_participant(self, message):
        await self._forward_message(message)

    async def add_vote(self, message):
        await self._forward_message(message)

    async def update_issue(self, message):
        await self._forward_message(message)

    async def chat_message(self, message):
        await self._forward_message(message)

    async def timer_start(self, message):
        await self._forward_message(message)

    async def timer_stop(self, message):
        await self._forward_message(message)

    async def reaction(self, message):
        await self._forward_message(message)

    async def update_room(self, message):
        await self._forward_message(message)
