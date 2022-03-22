from django.db import models
from src.oauth.models import User

from django.core.validators import FileExtensionValidator
from base.services import get_path_upload_post_image, validate_size_image


class PostTag(models.Model):
    """ Модель тегов, жанров
    """
    Tag = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Tags'
        verbose_name_plural = 'TagsXD'

    def __str__(self) -> str:
        return f'{self.Tag}'


class PostGame(models.Model):
    """ Модель постов
    """
    Email = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post_game')

    Title = models.CharField(max_length=200, unique=True)
    Description = models.TextField(max_length=10000, blank=True, null=True)

    PubDate = models.DateTimeField(auto_now_add=True)
    ChangeDate = models.DateTimeField(auto_now_add=True)

    Tags = models.ManyToManyField(PostTag)

    class Meta:
        verbose_name = 'Game Posts'
        verbose_name_plural = 'Game Posts'

    def __str__(self) -> str:
        return f'{self.Title}'


class PostImage(models.Model):
    """ Модель картинок поста
    """
    PostID = models.ForeignKey(
        PostGame, on_delete=models.CASCADE, related_name='post_images')

    Image = models.ImageField(
        upload_to=get_path_upload_post_image,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'gif', 'png']), validate_size_image]
    )

    class Meta:
        verbose_name = 'Post images'
        verbose_name_plural = 'Post images'

    def __str__(self) -> str:
        return f'{self.PostID}'


class PostLink(models.Model):
    """ Моднль ссылок поста
    """
    PostID = models.ForeignKey(
        PostGame, on_delete=models.CASCADE, related_name='post_links')

    Link = models.URLField()

    Image = models.ImageField(
        upload_to=get_path_upload_post_image,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'gif', 'png']), validate_size_image]
    )

    class Meta:
        verbose_name = 'Post links'
        verbose_name_plural = 'Post links'

    def __str__(self) -> str:
        return f'{self.PostID}'


class PostRating(models.Model):
    """ Модель звёздного рейтинга к посту
    """
    PostID = models.ForeignKey(
        PostGame, on_delete=models.CASCADE, related_name='rating_post')
    Email = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rating_user')

    Stars = models.SmallIntegerField()

    def __str__(self) -> str:
        return f'{self.PostID}'


class PostComment(models.Model):
    """ Модель комментариев к посту
    """
    PostID = models.ForeignKey(
        PostGame, on_delete=models.CASCADE, related_name='comment_post')
    Email = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment_user')

    Comment = models.TextField(max_length=2000, unique=True)

    class Meta:
        verbose_name = 'Post Comments'
        verbose_name_plural = 'Post Comments'

    def __str__(self) -> str:
        return f'{self.PostID}'


class CommentLikeDislike(models.Model):
    """ Модель лайков/дизлайков к комментарию
    """
    CommentID = models.ForeignKey(
        PostGame, on_delete=models.CASCADE, related_name='like_dislike_comment')
    Email = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='like_dislike_user')

    Status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Comment like/dislike'
        verbose_name_plural = 'Comment like/dislike'

    def __str__(self) -> str:
        return f'{self.CommentID}'


class UserBookmarks(models.Model):
    """ Модель закладок пользователя
        У одного пользователя может быть много постов (в закладках), 
        но это отдельностоящея таблица, чтобы не делать связь много ко многому в модели пользователя.
    """
    UserID = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    Bookmarks = models.ManyToManyField(PostTag)

    class Meta:
        verbose_name = 'User bookmarks'
        verbose_name_plural = 'User bookmarks'

    def __str__(self) -> str:
        return f'{self.UserID}'
