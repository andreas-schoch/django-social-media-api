from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.CreatePostView.as_view(), name='create-post'),
    path('<int:pk>/', views.GetUpdateDeletePostView.as_view(), name='get-update-delete-post'),
    path('likes/', views.ListUserLikedPostsView.as_view(), name='show-all-liked-posts'),
    path('likes/<int:pk>/', views.LikeOrUnlikePostView.as_view(), name='like-or-unlike-post'),
]
