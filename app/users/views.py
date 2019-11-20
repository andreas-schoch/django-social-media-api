from django.contrib.auth import get_user_model
from rest_framework import mixins, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404, CreateAPIView
from rest_framework.response import Response

from helpers.pagination import StandardResultsSetPagination
from .serializer import UserProfileSerializer, PublicUserSerializer, FollowSerializer
from .models import UserProfile, Follow
from helpers import my_mailer

# from helpers.permissions import IsOwnerOrReadOnly


User = get_user_model()


# # api/users/?search=<search_string>
# class SearchUsersView(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = PublicUserSerializer
#     filter_backends = (filters.SearchFilter,)
#     # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
#     search_fields = ('username',)
#     ordering = ('id',)


# api/users/
# api/users/?search=<username | email | first_name | last_name>
class GetAllUsersView(ListAPIView):
    """
    get: get ALL user profiles
    """
    pagination_class = StandardResultsSetPagination
    serializer_class = PublicUserSerializer
    queryset = User.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'email', 'first_name', 'last_name')


# api/users/<user_id>/
class GetUserProfileView(RetrieveAPIView):
    """
    get: get profile of specified user
    """
    lookup_field = 'user_id'
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


# api/users/follow/<user_id>
class FollowUnfollowUserView(CreateAPIView, mixins.DestroyModelMixin):
    """
    post: follow user with <user_id>
    delete: unfollow user with user_id
    """
    # lookup_field = 'user_id'  # not needed here but can be useful to replace 'pk' with something else
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def perform_create(self, serializer):
        user_to_follow = get_object_or_404(User, id=self.kwargs.get('user_id'))
        already_following = Follow.objects.filter(follower=self.request.user, followee=user_to_follow).exists()

        if already_following:
            raise PermissionDenied('already following')

        my_mailer.new_follower(user_to_follow, self.request.user)
        serializer.save(follower=self.request.user, followee=user_to_follow)

    def delete(self, request, *args, **kwargs):
        user_to_unfollow = get_object_or_404(User, id=self.kwargs.get('pk'))
        follow = get_object_or_404(Follow, follower=self.request.user, followee=user_to_unfollow)
        follow.delete()
        return Response(status=204)


# api/users/followers/
class GetUserFollowersView(ListAPIView):
    """
    get: get followers of logged in user
    """
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def get_queryset(self):
        return Follow.objects.filter(followee=self.request.user)


# api/users/following/
class GetUserFollowsView(ListAPIView):
    """
    get: get all users the logged in user follows
    """
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)



