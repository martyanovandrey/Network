
from django.urls import path

from . import views
'''
read it
https://stackoverflow.com/questions/51420143/django-pass-known-exact-string-as-a-url-parameter
'''
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:profile>", views.profile, name="profile"),

    # API Routes
    path("create_post", views.create_post, name="create_post"),
    path("posts/<str:postbox>", views.posts, name="posts"),
    path("follow", views.follow, name="follow"),
    path("user_api", views.user_api, name="user_api")
    
]
