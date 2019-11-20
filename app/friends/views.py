from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import ListAPIView, get_object_or_404, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from helpers.pagination import StandardResultsSetPagination
from users.serializer import FriendSerializer
from users.models import Friend, FriendStatus
from helpers.my_mailer import Mailer
from . import utils
# from helpers.permissions import IsOwnerOrReadOnly


User = get_user_model()


# api/users/friends/
class GetUserFriendsView(ListAPIView):
    """
    get: get a list of all friends of logged in user
    """
    pagination_class = StandardResultsSetPagination
    serializer_class = User
    queryset = User.objects.all()
    # queryset = Friend.objects.all()

    def get_queryset(self):
        # friends = utils.get_all_friends_from(self.request.user)
        friend_ids = utils.get_all_friend_user_ids_from(self.request.user)
        friends = User.objects.filter(sender__id=1)
        return friends


# api/users/friends/unfriend/<user_id>
class UnfriendUserView(DestroyAPIView):
    """
    delete: unfriend an user
    """
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    def delete(self, request, *args, **kwargs):
        friend = utils.get_friend_object_or_none(self.kwargs.get('user_id'), self.request.user.id)

        if not friend:
            raise NotFound('friend object not found')

        friend.delete()
        return Response(status=204)


# api/users/friends/requests/
class GetReceivedFriendRequests(ListAPIView):
    """
    get: get a list of all pending friend requests (send by others)
    """
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    def get_queryset(self):
        return Friend.objects.filter(receiver=self.request.user, status=FriendStatus.pending)


# api/users/friends/requests/pending/
class GetSendFriendRequests(ListAPIView):
    """
    get: get a list of all pending friend requests (send by the user)
    """
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    def get_queryset(self):
        return Friend.objects.filter(sender=self.request.user, status=FriendStatus.pending)


# api/users/friends/requests/<user_id>/
class SendFriendRequestView(CreateAPIView):
    """
    POST: send a friend request to another user
    """
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    def perform_create(self, serializer):
        # check if either user already send a friend request
        already_sent = Friend.objects.filter(
            (Q(sender=self.request.user) & Q(receiver=self.kwargs.get('user_id'))) |
            (Q(sender=self.kwargs.get('user_id')) & Q(receiver=self.request.user))
        ).exists()

        if already_sent:
            raise PermissionDenied('friend request already sent')

        receiving_user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        Mailer.pending_friend_request(receiving_user, self.request.user)
        serializer.save(sender=self.request.user, receiver=receiving_user)


# api/users/friends/requests/accept/<req_id>/
class AcceptFriendRequestView(UpdateAPIView):
    """
    put: set Friend status to accepted (patch works as well)
    if other user declines the request you cannot send him another one
    """
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    def update(self, request, *args, **kwargs):

        # notify sender via email that his friend request was accepted
        friend = get_object_or_404(Friend, id=self.kwargs.get('pk'))
        Mailer.friend_request_accepted(friend.receiver, friend.sender)

        # inject desired status
        request.data['status'] = FriendStatus.accepted
        return super().update(request, *args, **kwargs)


# api/users/friends/requests/reject/<req_id>/
class RejectFriendRequestView(UpdateAPIView):
    """
    patch: set status of Friend request to declined (put works as well)
    once its rejected the other user cannot spam you with more friend requests
    """
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    def update(self, request, *args, **kwargs):
        # inject desired status
        request.data['status'] = FriendStatus.declined
        return super().update(request, *args, **kwargs)

    # # this works as well but ONLY WITH PATCH
    # def partial_update(self, request, *args, **kwargs):
    #     print('TEST')
    #     request.data['status'] = FriendStatus.declined
    #     return self.update(request, *args, **kwargs)

