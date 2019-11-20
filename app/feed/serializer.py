from rest_framework import serializers
from feed.models import Post, Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post']


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'created', 'user', 'likes']
        read_only_fields = ['id', 'user', 'created']

    def get_likes(self, post):
        likes = post.likes.all()
        return LikeSerializer(likes, many=True).data




