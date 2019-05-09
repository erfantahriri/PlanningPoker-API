from rest_framework import serializers

from room.models import Room, Participant


class RoomSerializer(serializers.ModelSerializer):
    """Serialize Room model data."""

    uid = serializers.CharField(read_only=True)
    created = serializers.CharField(read_only=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Room
        fields = ('uid', 'title', 'description', 'updated', 'created',)


class JoinRoomInputSerializer(serializers.Serializer):
    """Input serializer for join room."""

    name = serializers.CharField(required=True)


class ParticipantSerializerWithToken(serializers.ModelSerializer):
    """Serialize Participant model data with access_token."""

    uid = serializers.CharField(read_only=True)
    created = serializers.CharField(read_only=True)

    class Meta:
        model = Participant
        fields = ('uid', 'name', 'access_token', 'created',)


class ParticipantSerializer(serializers.ModelSerializer):
    """Serialize Participant model data."""

    uid = serializers.CharField(read_only=True)
    created = serializers.CharField(read_only=True)

    class Meta:
        model = Participant
        fields = ('uid', 'name', 'created',)
