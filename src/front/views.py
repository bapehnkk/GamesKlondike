from django.shortcuts import render
from django.views.generic import DetailView
from src.oauth.models import User
from src.posts.models import PostGame

def home(request):
    alerts = []
    playlists = []
    cards = []
    for n in range(20):
        alerts.append({
            'text': 'Lorem'*50,
            'time': str((n+1)*2)+'min ago'
        })
        playlists.append({
            'text': n,
        })
        posts = PostGame.objects.all()
        print(posts[0].Email)

        cards.append({
            'title': posts[0].Title,
            'link': '/post/',
            'text': posts[0].Description,
            'date': posts[0].PubDate,
            'tags': [{
                'link': '/',
                'text': tag,
            } for tag in posts.all()[0].Tags.all()],
        })
    dict = {
        'alerts': alerts,
        'playlists': playlists,
        'cards': cards,

    }
    return render(request, 'front/home.html', dict)


def post(request):
    dict = {}
    return render(request, 'front/post.html', dict)


def login(request):
    dict = {}
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
    print('\r\n'*10)
    print(value)
    print('\r\n'*10)
    alerts = []
    playlists = []
    cards = []
    for n in range(20):
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

    }
    return render(request, 'card.html', dict)


def get_header_info(request) -> dict:
    header = {

    }
    return header