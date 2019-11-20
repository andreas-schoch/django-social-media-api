from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from feed.models import Post, Like
from feed.serializer import PostSerializer, LikeSerializer
from helpers.permissions import IsOwnerOrReadOnly
from helpers.custom_view_classes import CreateOrDestroyView
from friends.utils import get_all_friends_from
from helpers.my_mailer import Mailer



User = get_user_model()


# api/posts/<post_id>/
class GetUpdateDeletePostView(RetrieveUpdateDestroyAPIView):
    """
    get: get a single specific post. (Logged in users only)
    put: edit a post (owning user only).
    delete: delete a post (owning user only).
    """

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()


# api/posts/
class CreatePostView(CreateAPIView):
    """
    post: create a post (logged in, cannot create posts for other users)
    """
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        new_post = serializer.save(user=self.request.user)

        # notify all friends via email that user posted something
        Mailer.multi_friend_post_notification(new_post.user)




# api/posts/likes/
class ListUserLikedPostsView(ListAPIView):
    """
    get: a list of posts the requesting user liked
    """
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id)


# api/posts/like/<post_id>/
class LikeOrUnlikePostView(CreateOrDestroyView):
    """
    post: like post
    delete: unlike post
    """
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        already_liked = Like.objects.filter(user=self.request.user, post=post).exists()

        if already_liked:
            raise PermissionDenied('already liked')  # use ctrl+B to see more exceptions you could return
            # return Response(status=409)  # this does NOT return correct status code
        serializer.save(user=self.request.user, post=post)  # prevents "impersonating" other users

        # This works as well BUT it doesn't return the newly created like but {"user": Null, "post": Null }
        # like, created = Like.objects.get_or_create(user=self.request.user, post=post)
        # if not created:
        #     raise ValidationError('already liked', code=409)

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        like = get_object_or_404(Like, user=self.request.user, post=post)
        like.delete()
        return Response(status=204)
