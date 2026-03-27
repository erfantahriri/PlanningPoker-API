from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from room.models import Room, Participant, Issue, Vote
from room.validators import validate_estimated_points


class ParticipantSerializerWithToken(serializers.ModelSerializer):
    """Serialize Participant model data with access_token."""

    uid = serializers.CharField(read_only=True)
    created = serializers.CharField(read_only=True)

    class Meta:
        model = Participant
        fields = ('uid', 'name', 'role', 'access_token', 'created',)


class RoomSerializer(serializers.ModelSerializer):
    """Serialize Room model data."""

    uid = serializers.CharField(read_only=True)
    created = serializers.CharField(read_only=True)
    participant_count = serializers.SerializerMethodField()
    issue_count = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('uid', 'title', 'description', 'participant_count', 'issue_count', 'updated', 'created',)

    def get_participant_count(self, obj):
        return obj.participants.count()

    def get_issue_count(self, obj):
        return obj.issues.count()


class RoomSerializerWithToken(RoomSerializer):
    """Serialize Room model data with creator participant's access token."""

    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    creator_name = serializers.CharField(required=True, write_only=True)
    creator = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = ('uid', 'title', 'description', 'creator_name', 'creator',
                  'updated', 'created',)

    def validate_title(self, value):
        if Room.objects.filter(title=value).exists():
            raise ValidationError(["This Room title is already Taken."])
        return value

    def get_creator(self, obj):
        return ParticipantSerializerWithToken(instance=obj.creator).data


class JoinRoomInputSerializer(serializers.Serializer):
    """Input serializer for join room."""

    name = serializers.CharField(required=True)
    role = serializers.ChoiceField(
        choices=['voter', 'spectator'], default='voter', required=False
    )


class SubmitRoomCurrentIssueInputSerializer(serializers.Serializer):
    """Input serializer for set Room's current Issue."""

    issue_uid = serializers.CharField(required=True)


class ParticipantSerializer(serializers.ModelSerializer):
    """Serialize Participant model data."""

    uid = serializers.CharField(read_only=True)
    created = serializers.CharField(read_only=True)

    class Meta:
        model = Participant
        fields = ('uid', 'name', 'role', 'created',)


class VoteSerializer(serializers.ModelSerializer):
    """Serialize Vote model data."""

    participant = ParticipantSerializer()
    uid = serializers.CharField(read_only=True)
    created = serializers.CharField(read_only=True)

    class Meta:
        model = Vote
        fields = ('uid', 'participant', 'estimated_points', 'created',)


class IssueSerializer(serializers.ModelSerializer):
    """Serialize Issue model data."""

    title = serializers.CharField(required=True)
    uid = serializers.CharField(read_only=True)
    created = serializers.CharField(read_only=True)
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = ('uid', 'number', 'title', 'estimated_points',
                  'is_current', 'votes', 'vote_cards_status', 'created',)


class SubmitVoteInputSerializer(serializers.Serializer):
    """Input serializer for Submit Vote."""

    estimated_points = serializers.CharField(
        required=True, validators=[validate_estimated_points]
    )
