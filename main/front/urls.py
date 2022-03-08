from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('post/', views.post, name='post'), # условно, потом путь изменить
    path('login/', views.login, name='login'), 
    path('register/', views.register, name='register'), 
    path('profile/', views.profile, name='profile'), 
    path('profile/bookmark', views.profile_bookmark, name='profile_bookmark'), 
]
