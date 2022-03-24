from django.urls import path


from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('more_cards/', views.more_cards, name='more_cards'),
    path('post/<str:game>', views.post, name='post'), # условно, потом путь изменить
    
    path('login/', views.login, name='login'), 
    path('register/', views.register, name='register'), 
    path('logout/', views.logout_view, name='logout_view'),

    path('profile/', views.profile, name='profile'), 
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/notifications', views.profile_notifications, name='profile_notifications'), 
    path('profile/privacy', views.profile_privacy, name='profile_privacy'), 
    path('profile/bookmark', views.profile_bookmark, name='profile_bookmark'), 
]