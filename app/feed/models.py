from django.db import models
from django.contrib.auth import get_user_model

# from django.utils import timezone

User = get_user_model()


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30, blank=True)
    text = models.CharField(max_length=512, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)  # set related_name='posts' for reverse lookup
    # shared = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)  # TODO make sharing work
    # if related_name is not specified django will generate its own called "user.post_set"
    # if specified you can use User.posts as well as User.post_set
    # https://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django

    def __str__(self):
        return f'Posted by: {self.user}'

    def get_num_likes(self):
        return

    class Meta:
        ordering = ('created',)


class Like(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='liked_posts', null=True, blank=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)

