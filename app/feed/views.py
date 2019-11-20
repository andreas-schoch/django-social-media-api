from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.generics import ListAPIView

from friends import utils
from .serializer import PostSerializer
from feed.models import Post
from users.models import Follow
from helpers.pagination import StandardResultsSetPagination

User = get_user_model()  # https://wsvincent.com/django-referencing-the-user-model/


# api/feed/
# api/feed/?search=< username | title | text >
class ListPostsView(ListAPIView):
    """
    get: a paginated list of ALL posts by ALL users. Newest first
    """
    pagination_class = StandardResultsSetPagination
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'title', 'text')


# api/feed/<user_id>/
class ListUserPostsView(ListAPIView):
    """
    get: list all posts of a user
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        print(self.request.GET)  # this would print all querystring params
        posts = self.queryset.filter(user__id=self.kwargs.get("user_id"))
        return posts.order_by('-created')


# api/feed/followees/
class ListUserFollowingPostsView(ListAPIView):
    """
    get: list all posts of followed users
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        following = Follow.objects.filter(follower=self.request.user)
        followed_user_ids = [follow.followee.id for follow in following]
        posts = Post.objects.filter(user__in=followed_user_ids)
        return posts.order_by('-created')


# api/feed/friends/
class ListUserFriendPostsView(ListAPIView):
    """
    get: list all posts of users the logged in user befriended
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        friend_user_ids = utils.get_all_friend_user_ids_from(self.request.user)
        posts = Post.objects.filter(user__in=friend_user_ids)
        return posts.order_by('-created')
