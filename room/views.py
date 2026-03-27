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
                              SubmitRoomCurrentIssueInputSerializer)
from room.utils import broadcast_room_event


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
            defaults={"role": serializer.data.get("role", "voter")},
        )

        serializer = ParticipantSerializerWithToken(instance=participant)

        if created:
            broadcast_room_event(
                room.uid, 'add_participant',
                ParticipantSerializer(instance=participant).data
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
        return Issue.objects.filter(room=room).prefetch_related(
            'votes', 'votes__participant'
        )

    def perform_create(self, serializer):
        room = get_object_or_404(Room, uid=self.kwargs.get('room_uid'))
        serializer.validated_data['room_id'] = room.id
        issue = serializer.save()

        broadcast_room_event(
            room.uid, 'add_issue',
            IssueSerializer(instance=issue).data
        )


class RoomCurrentIssueAPIView(APIView):

    def get(self, request, room_uid):
        """Get Room's current Issue."""

        room = get_object_or_404(Room, uid=room_uid)

        if not room.current_issue:
            return Response(
                data={"details": "This room doesn't have a current issue."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = IssueSerializer(instance=room.current_issue)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, room_uid):
        """Set Room's current Issue."""

        room = get_object_or_404(Room, uid=room_uid)
        serializer = SubmitRoomCurrentIssueInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        issue = get_object_or_404(Issue, uid=serializer.data.get('issue_uid'),
                                  room__uid=room.uid)
        room.current_issue = issue
        room.save()

        serializer = IssueSerializer(instance=issue)
        broadcast_room_event(room.uid, 'current_issue', serializer.data)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class IssueAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsRoomParticipantPermission]
    serializer_class = IssueSerializer
    lookup_field = 'uid'

    def get_queryset(self):
        room = get_object_or_404(Room, uid=self.kwargs.get('room_uid'))
        return Issue.objects.filter(room=room).prefetch_related(
            'votes', 'votes__participant'
        )

    def perform_update(self, serializer):
        room = get_object_or_404(Room, uid=self.kwargs.get('room_uid'))
        issue = serializer.save()

        broadcast_room_event(
            room.uid, 'update_issue',
            IssueSerializer(instance=issue).data
        )


class VoteAPIView(APIView):

    permission_classes = [IsRoomParticipantPermission]

    def post(self, request, room_uid, issue_uid):
        """Submit a vote for a participant."""

        if request.participant.role == 'spectator':
            return Response(
                data={"detail": "Spectators cannot vote."},
                status=status.HTTP_403_FORBIDDEN
            )

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
        broadcast_room_event(room_uid, 'add_vote', serializer.data)

        if created:
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get(self, request, room_uid, issue_uid):
        """Get votes of an Issue."""

        issue = get_object_or_404(Issue, uid=issue_uid, room__uid=room_uid)
        votes = Vote.objects.filter(issue=issue).select_related('participant')
        serializer = VoteSerializer(instance=votes, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, room_uid, issue_uid):
        """Remove votes of an Issue."""

        issue = get_object_or_404(Issue, uid=issue_uid, room__uid=room_uid)
        Vote.objects.filter(issue=issue).delete()
        issue.vote_cards_status = settings.HIDDEN
        issue.save()

        broadcast_room_event(
            room_uid, 'update_issue',
            IssueSerializer(instance=issue).data
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
        broadcast_room_event(room_uid, 'update_issue', serializer.data)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
