from django.contrib.auth import get_user_model
from django.db import models
from annoying.fields import AutoOneToOneField
User = get_user_model()  # https://wsvincent.com/django-referencing-the-user-model/


class FriendStatus:
    pending = 'PENDING'
    accepted = 'ACCEPTED'
    declined = 'DECLINED'


FRIEND_CHOICES = (
    (FriendStatus.pending, 'PENDING'),
    (FriendStatus.accepted, 'ACCEPTED'),
    (FriendStatus.declined, 'DECLINED'),
)


class UserProfile(models.Model):
    user = AutoOneToOneField(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='profile',
        # editable=False
    )
    about = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.user)


class Interest(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='interests')
    interest = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return f'{self.user} is interested in {self.interest}'


# https://briancaffey.github.io/2017/07/19/different-ways-to-build-friend-models-in-django.html
class Follow(models.Model):
    follower = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='follower', null=True, blank=True)
    followee = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='followee',  null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.follower} follows {self.followee}'


class Friend(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sender', null=True, blank=True)
    receiver = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='receiver',  null=True, blank=True)
    status = models.CharField(max_length=9, choices=FRIEND_CHOICES, default=FriendStatus.pending)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'friend request from {self.sender} to {self.receiver}'


class Address(models.Model):
    user = AutoOneToOneField(to=User, on_delete=models.CASCADE, related_name='address')
    street = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    zip = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}, {self.street}, {self.city} {self.zip}, {self.country}'

