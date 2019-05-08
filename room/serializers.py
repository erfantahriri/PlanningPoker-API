from rest_framework import serializers

from room.models import Room


class RoomSerializer(serializers.ModelSerializer):
    """Serialize Room model data."""

    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Room
        fields = ('uid', 'title', 'description', 'updated', 'created',)
