from django.urls import path


from src.posts import views as views_posts
from src.oauth import views as views_oauth
from src.parser import parser_view as p_v

urlpatterns = [
    path('', views_posts.home, name='home'),
    path('more_cards/<int:post_count>', views_posts.more_cards, name='more_cards'),
    
    path('post/<str:game>', views_posts.post, name='post'),
    
    path('login/', views_oauth.login, name='login'), 
    path('register/', views_oauth.register, name='register'), 
    path('logout/', views_oauth.logout_view, name='logout_view'),

    path('profile/', views_oauth.profile, name='profile'), 
    path('profile/edit', views_oauth.profile_edit, name='profile_edit'),
    path('profile/password', views_oauth.profile_password, name='profile_password'),
    path('profile/notifications', views_oauth.profile_notifications, name='profile_notifications'), 
    path('profile/privacy', views_oauth.profile_privacy, name='profile_privacy'), 
    path('profile/bookmark', views_oauth.profile_bookmark, name='profile_bookmark'), 

    path('parser/', p_v.ParserView.as_view(), name='parser'), 
    path('parser/start', p_v.ParserView.as_view(), name='parser_start'), 
    # path('parser/start', p_v.ParserView.as_view(), name=''), 
]