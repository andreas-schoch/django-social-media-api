from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from .models import UserProfile, Follow, Interest, Friend, FriendStatus, Address
from drf_writable_nested import WritableNestedModelSerializer

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followee']
        read_only = True


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['id', 'sender', 'receiver', 'status']
        read_only_fields = ['id', 'sender', 'receiver']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['user', 'interest']
        read_only_fields = ['user']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'street', 'city', 'zip', 'country']
        read_only_fields = ['id', 'user']


class UserProfileSerializer(serializers.ModelSerializer):
    # interests = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('about', 'phone')
        # read_only_fields = ['id', 'user']

    # def get_interests(self, user):
    #     inter = user.interests.all()
    #     return InterestSerializer(inter, many=True).data


class PrivateUserSerializer(WritableNestedModelSerializer):
    profile = UserProfileSerializer()
    address = AddressSerializer(read_only=False)
    interests = InterestSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile', 'address', 'interests']
        # read_only = True


# class PrivateUserSerializer(serializers.ModelSerializer):
#     profile = UserProfileSerializer()
#     class Meta:
#         model = User
#         fields = '__all__'
#         read_only_fields = ('password', 'id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined',
#                             'groups, user_permissions')


class PublicUserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()  # users that follow this user
    following = serializers.SerializerMethodField()  # users the user follows
    friends = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    # followers = FollowSerializer(many=True, read_only=True)  # not working

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'address', 'followers', 'following', 'friends']

    def get_profile(self, profile):
        # profiles = UserProfile.objects.get(user=profile.user)
        return UserProfileSerializer(profile).data

    def get_address(self, user):
        return AddressSerializer(user.address).data

    def get_followers(self, user):
        follows = user.followee.all()  # get all Follows where 'followee' references this user
        return FollowSerializer(follows, many=True).data

    def get_following(self, user):
        follows = user.follower.all()  # get all Follows where 'follower' references this user
        return FollowSerializer(follows, many=True).data

    def get_friends(self, user):
        # gets all accepted Friend objects where logged in user is mentioned
        friends = Friend.objects.filter((Q(sender=user) | Q(receiver=user)) & Q(status=FriendStatus.accepted))
        return FriendSerializer(friends, many=True).data










