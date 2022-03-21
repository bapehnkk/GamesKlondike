from django.db import models
from django.core.validators import FileExtensionValidator

from base.services import get_path_upload_avatar, validate_size_image

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)



class UserManager(BaseUserManager):
    def create_user(self, Email, password=None, **kwargs):
        if not Email:
            raise ValueError('Users must have an Email')

        user = self.model(
            Email=Email, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Email, password):
        """ Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            Email,
            password=password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Кастомная модель пользователя | Custom User model
    """
    Email = models.EmailField(unique=True)
    UserName = models.CharField(max_length=200, unique=True)

    JoinDate = models.DateTimeField(auto_now_add=True)
    LastDate = models.DateTimeField(auto_now_add=True)

    JoinIP = models.CharField(max_length=200)
    LastIP = models.CharField(max_length=200)

    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'png']), validate_size_image]
    )

    objects = UserManager()

    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = []

    @property
    def is_staff(self):
        return self.Email

    def __str__(self):
        return self.Email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'

