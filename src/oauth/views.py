from django.shortcuts import redirect, render
from django.contrib import auth

from django.contrib.auth.decorators import login_required
from base.services import get_client_ip

from src.oauth.forms import UserRegForm
from src.oauth.models import User

@login_required
def logout_view(request):
    """ Выход из учётной записи
    """
    if request.session._session != {}:
        auth.logout(request)
    return redirect('/')


def login(request):
    if request.session._session != {}:
        return redirect('/')
    if request.method == 'POST':
        Email = request.POST['Email']
        Password = request.POST['Password']
        user = auth.authenticate(username=Email, password=Password)
        if user is not None and user.is_active:
            # Правильный пароль и пользователь "активен"
            auth.login(request, user)
            # Перенаправление на "правильную" страницу
            return redirect("/")
        else:
            # Отображение страницы с ошибкой
            dict = {
                'errors': 'Invalid Email or Password'
            }
            return render(request, 'front/login.html', dict)
    return render(request, 'front/login.html', {})


def register(request):
    if request.session._session != {}:
        return redirect('/')

    if request.method == 'POST':
        form = UserRegForm(request.POST, request.FILES or None)
        
        # Сохранить пользователя    
        if User().create(request=request, form=form):
            # Вход
            user = auth.authenticate(Email=form.cleaned_data.get('Email'),
                                     password=form.cleaned_data.get('Password'))
            if user is not None and user.is_active :
                # Правильный пароль и пользователь "активен"
                auth.login(request, user)
                # Перенаправление на "правильную" страницу
                return redirect("/")
            else:
                # Отображение страницы с ошибкой
                return redirect("/Error404")
        else:
            dict = {
                'form': UserRegForm(),
                'errors': form.errors
            }
            return render(request, 'front/register.html', dict)
    dict = {
        'form': UserRegForm()
    }
    return render(request, 'front/register.html', dict)


@login_required
def profile(request):
    dict = {
        'profile_if': 'AccountOverview',
    }
    return render(request, 'front/profile.html', dict)


@login_required
def profile_edit(request):
    dict = {
        'profile_if': 'edit',
    }
    return render(request, 'front/profile.html', dict)


@login_required
def profile_notifications(request):
    dict = {
        'profile_if': 'notifications',
    }
    return render(request, 'front/profile.html', dict)


@login_required
def profile_privacy(request):
    dict = {
        'profile_if': 'privacy',
    }
    return render(request, 'front/profile.html', dict)


@login_required
def profile_bookmark(request):
    alerts = []
    playlists = []
    cards = []
    for n in range(5):
        alerts.append({
            'text': 'Lorem'*50,
            'time': str((n+1)*2)+'min ago'
        })
        playlists.append({
            'text': n,
        })
        cards.append({
            'title': 'Title'+str(n+1),
            'link': '/post/',
            'text': ('Text'+str(n+1))*100,
            'date': 'date'+str(n+1),
            'tags': [{
                'link': '/',
                'text': 'tag'+str(n+1),
            },
                {'link': '/', 'text': 'tag'+str(n+1), }
            ],
        })
    dict = {
        'alerts': alerts,
        'playlists': playlists,
        'cards': cards,
        'profile_if': 'bookmark',
    }
    return render(request, 'front/profile.html', dict)

