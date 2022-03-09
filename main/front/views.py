from django.shortcuts import render


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
        cards.append({
            'title': 'Title'+str(n+1),
            'link': '/post/',
            'text': ('Text'+str(n+1))*100,
            'date': 'date'+str(n+1),
            'tags': [{
                'link': '/',
                'text': 'tag'+str(n+1),
            },
            {'link': '/','text': 'tag'+str(n+1),}
            ],
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
    dict = {}
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
            {'link': '/','text': 'tag'+str(n+1),}
            ],
        })
    dict = {
        'alerts': alerts,
        'playlists': playlists,
        'cards': cards,
        'profile_if': 'bookmark',
    }
    return render(request, 'front/profile.html', dict)

def more_post(request):
    
