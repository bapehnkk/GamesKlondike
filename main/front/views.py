from django.shortcuts import render

def home(request):
    dict = {
        'allerts': [(n+1)*2 for n in range(20)],
    }
    return render(request, 'front/home.html', dict)
