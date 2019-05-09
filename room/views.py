from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, get_object_or_404,
                                     ListAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from room.models import Room, Participant, Issue
from room.serializers import (RoomSerializer, JoinRoomInputSerializer,
                              ParticipantSerializerWithToken,
                              ParticipantSerializer, IssueSerializer)


class RoomAPIView(ListCreateAPIView):

    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class JoinRoomAPIView(APIView):
    """Add new participant for a room."""

    def post(self, request, room_uid):

        room = get_object_or_404(Room, uid=room_uid)
        serializer = JoinRoomInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        participant, created = Participant.objects.get_or_create(
            room=room,
            name=serializer.data.get("name"),
        )

        serializer = ParticipantSerializerWithToken(instance=participant)

        if created:
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RoomParticipantsListAPIView(ListAPIView):

    serializer_class = ParticipantSerializer
    pagination_class = None

    def get_queryset(self):
        room = get_object_or_404(Room, uid=self.kwargs.get('room_uid'))
        return Participant.objects.filter(room=room)


class RoomIssueAPIView(ListCreateAPIView):

    serializer_class = IssueSerializer
    pagination_class = None

    def get_queryset(self):
        room = get_object_or_404(Room, uid=self.kwargs.get('room_uid'))
        return Issue.objects.filter(room=room)

    def perform_create(self, serializer):
        room = get_object_or_404(Room, uid=self.kwargs.get('room_uid'))
        serializer.validated_data['room_id'] = room.id
        serializer.save()
