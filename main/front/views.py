from django.shortcuts import render


def home(request):
    allerts = []
    playlists = []
    for n in range(20):
        allerts.append({
            'text': 'Lorem'*50,
            'time': str((n+1)*2)+'min ago'
        })
        playlists.append({
            'text': n,
        })
    dict = {
        'allerts': allerts,
        'playlists': playlists,

    }
    return render(request, 'front/home.html', dict)
