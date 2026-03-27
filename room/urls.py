from django.urls import path

from room import views

urlpatterns = [
    path('', views.RoomAPIView.as_view(), name='rooms'),
    path('<str:room_uid>/info', views.RoomInfoAPIView.as_view(), name='room_info'),
    path('<str:room_uid>/summary', views.RoomSummaryAPIView.as_view(), name='room_summary'),
    path('<str:room_uid>/join', views.JoinRoomAPIView.as_view(),
         name='join_room'),
    path('<str:room_uid>/participants',
         views.RoomParticipantsListAPIView.as_view(),
         name='room_participants'),
    path('<str:room_uid>/participants/<str:participant_uid>',
         views.ParticipantSelfUpdateAPIView.as_view(),
         name='participant_self_update'),
    path('<str:room_uid>/issues', views.RoomIssueAPIView.as_view(),
         name='room_issues'),
    path('<str:room_uid>/current_issue',
         views.RoomCurrentIssueAPIView.as_view(), name='room_current_issue'),
    path('<str:room_uid>/issues/<str:uid>',
         views.IssueAPIView.as_view(), name='room_issue'),
    path('<str:room_uid>/issues/<str:issue_uid>/votes',
         views.VoteAPIView.as_view(), name='room_issue_votes'),
    path('<str:room_uid>/issues/<str:issue_uid>/votes/flip',
         views.FlipIssueVoteCardsAPIView.as_view(),
         name='room_issue_flip_votes'),
]
