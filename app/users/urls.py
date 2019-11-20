from django.urls import path, include
from . import views

app_name = 'users'


urlpatterns = [
    path('', views.GetAllUsersView.as_view(), name="list-all-users"),
    path('<int:user_id>/', views.GetUserProfileView.as_view(), name="get-single-user-profile"),
    path('follow/<int:user_id>/', views.FollowUnfollowUserView.as_view(), name="follow-unfollow-a-user"),
    path('followers/', views.GetUserFollowersView.as_view(), name='get-followers-of-logged-in-user'),
    path('following/', views.GetUserFollowsView.as_view(), name='get-users-the-logged-in-user-follows'),
    path('friends/', include('friends.urls'))
    # TODO add endpoints for interest model
]
