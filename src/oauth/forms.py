from .models import User
from django.forms import EmailField, EmailInput, Form, CharField, ImageField, PasswordInput, ClearableFileInput, TextInput


class UserRegForm(Form):
    Email = EmailField(widget=EmailInput(attrs={
        'class': 'auth__input',
        'placeholder': 'Email',
    }))
    UserName = CharField(widget=TextInput(attrs={
        'class': 'auth__input',
        'placeholder': 'UserName',
    }))
    Password = CharField(widget=PasswordInput(attrs={
        'class': 'auth__input',
    }))
    Avatar = ImageField(widget=ClearableFileInput(attrs={
            'class': 'auth__input',
    }))
