from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('', views.ListPostsView.as_view(), name='show-all-posts'),
    path('<int:user_id>/', views.ListUserPostsView.as_view(), name='list-user-posts'),
    path('followees/', views.ListUserFollowingPostsView.as_view(), name='list-posts-of-followed-users'),
    path('friends/', views.ListUserFriendPostsView.as_view(), name='list-posts-of-friends'),
]
