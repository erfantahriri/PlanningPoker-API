from django.urls import path

from room import views

urlpatterns = [
    path('', views.RoomAPIView.as_view()),
    path('<str:room_uid>/join', views.JoinRoomAPIView.as_view(),
         name='join_room'),
    path('<str:room_uid>/participants',
         views.RoomParticipantsListAPIView.as_view()),
    path('<str:room_uid>/issues', views.RoomIssueAPIView.as_view()),
]
