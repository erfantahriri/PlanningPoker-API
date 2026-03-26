from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_room_event(room_uid, event_type, content):
    """Send a group event to all WebSocket clients connected to a room."""
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        'room_{}'.format(room_uid),
        {'type': event_type, 'content': content}
    )
