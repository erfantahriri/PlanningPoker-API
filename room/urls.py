from django.urls import path

from room import views

urlpatterns = [
    path('', views.RoomAPIView.as_view()),
]
