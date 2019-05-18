from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, get_object_or_404,
                                     RetrieveUpdateDestroyAPIView,
                                     ListAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from room.models import Room, Participant, Issue, Vote
from room.permissions import IsRoomParticipantPermission
from room.serializers import (RoomSerializer, JoinRoomInputSerializer,
                              ParticipantSerializerWithToken,
                              ParticipantSerializer, IssueSerializer,
                              SubmitVoteInputSerializer, VoteSerializer, RoomSerializerWithToken)


class RoomAPIView(ListCreateAPIView):

    queryset = Room.objects.all()

    def perform_create(self, serializer):
        creator_name = serializer.validated_data.pop("creator_name")
        room = serializer.save()
        Participant.objects.create(
            room=room,
            name=creator_name,
            is_creator=True
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RoomSerializerWithToken
        return RoomSerializer


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

    permission_classes = [IsRoomParticipantPermission]
    serializer_class = ParticipantSerializer
    pagination_class = None

    def get_queryset(self):
        room = get_object_or_404(Room, uid=self.kwargs.get('room_uid'))
        return Participant.objects.filter(room=room)


class RoomIssueAPIView(ListCreateAPIView):

    permission_classes = [IsRoomParticipantPermission]
    serializer_class = IssueSerializer
    pagination_class = None

    def get_queryset(self):
        room = get_object_or_404(Room, uid=self.kwargs.get('room_uid'))
        return Issue.objects.filter(room=room)

    def perform_create(self, serializer):
        room = get_object_or_404(Room, uid=self.kwargs.get('room_uid'))
        serializer.validated_data['room_id'] = room.id
        serializer.save()

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            'room_{room_uid}'.format(room_uid=room.uid),
            {
                'type': 'send_message',
                'content': 'New Issue Added!!!'
            }
        )


class IssueAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsRoomParticipantPermission]
    serializer_class = IssueSerializer
    lookup_field = 'uid'

    def get_queryset(self):
        room = get_object_or_404(Room, uid=self.kwargs.get('room_uid'))
        return Issue.objects.filter(room=room)


class VoteAPIView(APIView):

    permission_classes = [IsRoomParticipantPermission]

    def post(self, request, room_uid, issue_uid):
        """Submit a vote for a participant."""

        issue = get_object_or_404(Issue, uid=issue_uid, room__uid=room_uid)

        serializer = SubmitVoteInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vote, created = Vote.objects.get_or_create(
            issue=issue,
            participant=request.participant
        )

        vote.estimated_points = serializer.data.get('estimated_points')
        vote.save()

        if created:
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_200_OK)

    def get(self, request, room_uid, issue_uid):
        """Get votes of an Issue."""

        issue = get_object_or_404(Issue, uid=issue_uid, room__uid=room_uid)
        votes = Vote.objects.filter(issue=issue)
        serializer = VoteSerializer(instance=votes, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
