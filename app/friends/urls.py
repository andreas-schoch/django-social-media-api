from django.urls import path
from . import views

app_name = 'friends'


urlpatterns = [
    path('', views.GetUserFriendsView.as_view(), name='get-friends-of-logged-in-user'),
    path('unfriend/<int:user_id>/', views.UnfriendUserView.as_view(), name='unfriend-another-user'),
    path('requests/', views.GetReceivedFriendRequests.as_view(), name='get-pending-friend-requests-received'),
    path('requests/pending/', views.GetSendFriendRequests.as_view(), name='get-pending-friend-requests-sent'),
    path('requests/<int:user_id>/', views.SendFriendRequestView.as_view(), name='send-friend-request'),
    path('requests/accept/<int:pk>/', views.AcceptFriendRequestView.as_view(), name='accept-new-friend'),
    path('requests/reject/<int:pk>/', views.RejectFriendRequestView.as_view(), name='reject-new-friend'),
]
