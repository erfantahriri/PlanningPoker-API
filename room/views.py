from rest_framework.generics import ListCreateAPIView

from room.models import Room
from room.serializers import RoomSerializer


class RoomAPIView(ListCreateAPIView):

    serializer_class = RoomSerializer
    queryset = Room.objects.all()
