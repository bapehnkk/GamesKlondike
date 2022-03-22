from django.contrib import admin

from .models import PostGame, PostImage, PostLink, PostComment, CommentLikeDislike, PostRating, UserBookmarks

admin.site.register(PostGame)
admin.site.register(PostImage)
admin.site.register(PostLink)
admin.site.register(PostComment)
admin.site.register(CommentLikeDislike)
admin.site.register(PostRating)
admin.site.register(UserBookmarks)