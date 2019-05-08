from rest_framework import serializers

from room.models import Room, Participant


class RoomSerializer(serializers.ModelSerializer):
    """Serialize Room model data."""

    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Room
        fields = ('uid', 'title', 'description', 'updated', 'created',)


class JoinRoomInputSerializer(serializers.Serializer):
    """Input serializer for join room."""

    name = serializers.CharField(required=True)


class ParticipantSerializerWithToken(serializers.ModelSerializer):
    """Serialize Participant model data."""

    class Meta:
        model = Participant
        fields = ('uid', 'name', 'access_token', 'created',)
