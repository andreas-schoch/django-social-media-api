from annoying.functions import get_object_or_None
from django.db.models import Q

from users.models import Friend, FriendStatus


def get_all_friends_from(user):
    """
    get all Friend instances where user is either sender or receiver
    """
    condition = (Q(sender=user) | Q(receiver=user)) & Q(status=FriendStatus.accepted)
    return Friend.objects.filter(condition)


def get_all_friend_user_ids_from(user):
    """
    get all user ids from friends
    """
    friends = get_all_friends_from(user)

    friend_user_ids = set()
    for friend in friends:
        if friend.sender.id != user.id:
            friend_user_ids.add(friend.sender.id)

        if friend.receiver.id != user.id:
            friend_user_ids.add(friend.receiver.id)

    return friend_user_ids


def get_friend_object_or_none(user1_id, user2_id):
    """
    get a single Friend instance or None returned
    """
    condition = Q(sender=user1_id) & Q(receiver=user2_id) | Q(sender=user2_id) & Q(receiver=user1_id)
    return get_object_or_None(Friend, condition)
