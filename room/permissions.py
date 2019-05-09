import jwt
from django.conf import settings
from jwt import InvalidSignatureError, DecodeError
from rest_framework import permissions

from room.models import Participant


class IsRoomParticipantPermission(permissions.BasePermission):
    """
    permission for check participant.
    """

    def has_permission(self, request, view):

        try:
            payload = jwt.decode(request.META.get('HTTP_AUTHORIZATION'),
                                 key=settings.JWT_SECRET_KEY)
            request.participant = Participant.objects.get(
                uid=payload.get('participant_uid')
            )
            if request.participant.room.uid != view.kwargs.get('room_uid'):
                return False

        except (KeyError, InvalidSignatureError, DecodeError):
            return False

        return True
