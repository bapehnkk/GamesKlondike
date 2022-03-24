from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from src.oauth.models import User
from src.posts.models import PostGame
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib import auth



def logout_view(request):
    """ Выход из учётной записи
    """
    if request.session._session != {}:
        logout(request)
    return redirect('/')

def home(request):
    """ Home/Index page
    """
    if request.GET:
        search = request.GET.get('search')
    else:
        search = ''

    dict = {
        'header': get_header_content(request),
        'cards': get_cards(search),
    }
    return render(request, 'front/home.html', dict)


try:
    """ Этот try для моментов когда удаляется DB и нужно сделать новые миграции
        Берётся первая запись из бд. 
        Если бд нет, то невозможно применить миграции. =)
    """
    def post(request, game=PostGame.objects.all()[0].id):
        dict = get_post_by_id(game)
        return render(request, 'front/post.html', dict)
except:
    """ На релизе удалить, или как-то пофиксить. =)
    """
    def post(request, game=0):
        dict = get_post_by_id(game)
        return render(request, 'front/post.html', dict)


def login(request):
    if request.session._session != {}:
       return redirect('/')
    dict = {}
    if request.method == 'POST':
        Email = request.POST['Email']
        Password = request.POST['Password']
        user = auth.authenticate(username=Email, password=Password)
        print(f'\r\n{user}\r\n')
        if user is not None and user.is_active:
            # Правильный пароль и пользователь "активен"
            auth.login(request, user) 
            # Перенаправление на "правильную" страницу
            return redirect("/")
        else:
            # Отображение страницы с ошибкой
            return redirect("/Error404")
    return render(request, 'front/login.html', dict)


def register(request):
    dict = {}
    return render(request, 'front/register.html', dict)


def profile(request):
    dict = {
        'profile_if': 'AccountOverview',
    }
    return render(request, 'front/profile.html', dict)


def profile_edit(request):
    dict = {
        'profile_if': 'edit',
    }
    return render(request, 'front/profile.html', dict)


def profile_notifications(request):
    dict = {
        'profile_if': 'notifications',
    }
    return render(request, 'front/profile.html', dict)


def profile_privacy(request):
    dict = {
        'profile_if': 'privacy',
    }
    return render(request, 'front/profile.html', dict)


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


class CardsDetailView(DetailView):
    pass


def more_cards(request, value=0):
    alerts = []
    playlists = []
    cards = get_cards()
    for n in range(20):
        alerts.append({
            'text': 'Lorem'*50,
            'time': str((n+1)*2)+'min ago'
        })
        playlists.append({
            'text': n,
        })
    dict = {
        'alerts': alerts,
        'playlists': playlists,
        'cards': cards,

    }
    return render(request, 'card.html', dict)


def get_header_info(request) -> dict:
    header = {}
    return header


def get_cards(selector='') -> list:
    """ Взять все посты из БД и отдать в виде массива
    """
    cards = ([{
        'title': f'{post.Title} id:{post.id}',
        'images': (post.post_images.all()),
        'link': f'/post/{post.id}',
        'text': f'{post.Description}',
        'date': post.PubDate,
        'tags': ([{
                'link': f'/{tag}',
                'text': f'{tag}',
        } for tag in post.Tags.all()]),
    } for post in PostGame.objects.filter(
        Q(Title__contains=selector) | Q(Description__contains=selector))])

    return cards


def get_post_by_id(id: int) -> dict:
    """ Взять пост из БД 
    """
    post = PostGame.objects.get(id=id)
    post = {
        'title': f'{post.Title} id:{post.id}',
        'images': post.post_images.all(),
        'links': post.post_links.all(),
        'text': post.Description,

        'publisher': {
            'date': post.PubDate,
            'link': f'/user/{post.Email.id}',
            'user': post.Email.UserName, },

        'tags': ([{
            'link': f'/tag/{tag}',
            'text': tag,
        } for tag in post.Tags.all()]),

        'comments': ([{
            'text': comment.Text,
            'date': comment.PubDate,
            'user': comment.Email.UserName,
            'link': f'/user/{comment.Email.id}',
            'likes': f'{comment.like_dislike_comment.filter(Status=True).count()}',
            'dislikes': f'{comment.like_dislike_comment.filter(Status=False).count()}',
        } for comment in post.comment_post.all()])
    }

    return post

def get_header_content(request) -> dict:
    if request.session._session == {}:
        return {}

    header = {
        'alerts': get_alerts(),
        # 'playlists': []   # мб не надо, но когда-нибудь можно запилить
    }
    return header

def get_alerts() -> tuple:
    alerts = []
    for n in range(20):
        alerts.append({
            'image': 'img/no-image.png',
            'text': f'This is {n+1}\'s alert',
            'time': f'{timezone.now()}'
        })
    return tuple(alerts)