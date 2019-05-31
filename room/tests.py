from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from room.models import Room
from room.serializers import RoomSerializer, RoomSerializerWithToken

# initialize the APIClient app
client = Client()


class GetAllRoomsTest(TestCase):
    """ Test module for GET all Rooms API """

    def setUp(self):
        Room.objects.create(
            title="Test Room",
            description="test room test room"
        )

    def test_get_all_rooms(self):
        response = client.get(reverse('rooms'))
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateRoomTest(TestCase):
    """ Test module for Post Rooms API """

    def test_create_new_room(self):
        response = self.client.post(
            reverse('rooms'), data={
                "title": "Test Room",
                "description": "test room test room",
                "creator_name": "Test Creator"
            }
        )
        room = Room.objects.first()
        serializer = RoomSerializerWithToken(room)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
