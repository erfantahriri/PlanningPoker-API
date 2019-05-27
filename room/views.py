from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
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
                              SubmitVoteInputSerializer, VoteSerializer,
                              RoomSerializerWithToken,
                              SubmitRoomCurrentIsseueInputSerializer)


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
            layer = get_channel_layer()
            async_to_sync(layer.group_send)(
                'room_{room_uid}'.format(room_uid=room.uid),
                {
                    'type': 'add_participant',
                    'content': ParticipantSerializer(instance=participant).data
                }
            )
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
        issue = serializer.save()

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            'room_{room_uid}'.format(room_uid=room.uid),
            {
                'type': 'add_issue',
                'content': IssueSerializer(instance=issue).data
            }
        )


class RoomCurrentIssueAPIView(APIView):

    def get(self, request, room_uid):
        """Get Room's current Issue."""

        room = get_object_or_404(Room, uid=room_uid)

        if not room.current_issue:
            return Response(
                data={
                    "details": "This room is don't have any current issue now"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = IssueSerializer(instance=room.current_issue)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, room_uid):
        """Set Room's current Issue."""

        room = get_object_or_404(Room, uid=room_uid)
        serializer = SubmitRoomCurrentIsseueInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        issue = get_object_or_404(Issue, uid=serializer.data.get('issue_uid'),
                                  room__uid=room.uid)
        room.current_issue = issue
        room.save()

        serializer = IssueSerializer(instance=issue)

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            'room_{room_uid}'.format(room_uid=room.uid),
            {
                'type': 'current_issue',
                'content': serializer.data
            }
        )

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class IssueAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsRoomParticipantPermission]
    serializer_class = IssueSerializer
    lookup_field = 'uid'

    def get_queryset(self):
        room = get_object_or_404(Room, uid=self.kwargs.get('room_uid'))
        return Issue.objects.filter(room=room)

    def perform_update(self, serializer):
        room = get_object_or_404(Room, uid=self.kwargs.get('room_uid'))
        issue = serializer.save()

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            'room_{room_uid}'.format(room_uid=room.uid),
            {
                'type': 'update_issue',
                'content': IssueSerializer(instance=issue).data
            }
        )


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

        serializer = VoteSerializer(instance=vote)

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            'room_{room_uid}'.format(room_uid=room_uid),
            {
                'type': 'add_vote',
                'content': serializer.data
            }
        )

        if created:
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get(self, request, room_uid, issue_uid):
        """Get votes of an Issue."""

        issue = get_object_or_404(Issue, uid=issue_uid, room__uid=room_uid)
        votes = Vote.objects.filter(issue=issue)
        serializer = VoteSerializer(instance=votes, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, room_uid, issue_uid):
        """Remove votes of an Issue."""

        issue = get_object_or_404(Issue, uid=issue_uid, room__uid=room_uid)
        Vote.objects.filter(issue=issue).delete()
        issue.vote_cards_status = settings.HIDDEN
        issue.save()

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            'room_{room_uid}'.format(room_uid=room_uid),
            {
                'type': 'update_issue',
                'content': IssueSerializer(instance=issue).data
            }
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class FlipIssueVoteCardsAPIView(APIView):

    permission_classes = [IsRoomParticipantPermission]

    def post(self, request, room_uid, issue_uid):
        """Flip an Issue's Vote cards."""

        issue = get_object_or_404(Issue, uid=issue_uid, room__uid=room_uid)

        if issue.vote_cards_status == settings.HIDDEN:
            issue.vote_cards_status = settings.VISIBLE
        else:
            issue.vote_cards_status = settings.HIDDEN
        issue.save()

        serializer = IssueSerializer(instance=issue)

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            'room_{room_uid}'.format(room_uid=room_uid),
            {
                'type': 'update_issue',
                'content': serializer.data
            }
        )

        return Response(data=serializer.data, status=status.HTTP_200_OK)
