from django.contrib import admin

# Register your models here.
from .models import Post, Like
#
# admin.site.register(Post)
# admin.site.register(Like)


# @admin.register(Like)
class LikeInline(admin.TabularInline):
    model = Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        LikeInline
    ]


