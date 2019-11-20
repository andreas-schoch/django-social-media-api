from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import UserProfile, Follow, Friend, Interest, Address
from feed.models import Post

User = get_user_model()


class UserProfileInline(admin.TabularInline):
    model = UserProfile


class FollowersInline(admin.TabularInline):
    model = Follow
    fk_name = 'followee'


class FollowingInline(admin.TabularInline):
    model = Follow
    fk_name = 'follower'


class UserPostsInline(admin.TabularInline):
    model = Post


class AddressInline(admin.TabularInline):
    model = Address


# class FriendSenderInline(admin.TabularInline):
#     model = Friend
#     fk_name = 'sender'
#
#
# class FriendReceiverInline(admin.TabularInline):
#     model = Friend
#     fk_name = 'receiver'


admin.site.unregister(User)  # need to unregister user to add profile as inline
admin.site.register(Follow)
admin.site.register(Friend)
admin.site.register(Interest)


@admin.register(User)  # does the same as admin.site.register
class PostAdmin(admin.ModelAdmin):
    inlines = [
        UserProfileInline,
        AddressInline,
        FollowersInline,
        FollowingInline,
        UserPostsInline,
        # FriendSenderInline,
        # FriendReceiverInline,
    ]

