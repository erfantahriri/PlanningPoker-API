from rest_framework import serializers

from room.models import Room, Participant, Issue, Vote
from room.validators import validate_estimated_points


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


class IssueSerializer(serializers.ModelSerializer):
    """Serialize Issue model data."""

    uid = serializers.CharField(read_only=True)
    created = serializers.CharField(read_only=True)
    title = serializers.CharField(required=True)

    class Meta:
        model = Issue
        fields = ('uid', 'number', 'title', 'estimated_points', 'created',)


class SubmitVoteInputSerializer(serializers.Serializer):
    """Input serializer for Submit Vote."""

    estimated_points = serializers.CharField(
        required=True, validators=[validate_estimated_points]
    )


class VoteSerializer(serializers.ModelSerializer):
    """Serialize Vote model data."""

    participant = ParticipantSerializer()
    uid = serializers.CharField(read_only=True)
    created = serializers.CharField(read_only=True)

    class Meta:
        model = Vote
        fields = ('uid', 'participant', 'estimated_points', 'created',)
