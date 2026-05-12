"""
URL configuration for movie_recommender project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recommender import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('', views.home, name='home'),
path('trending/', views.trending, name='trending'),
    path('recommend/', views.recommend_view, name='recommend'),
    path('user-recommend/', views.user_recommendations, name='user_recommend'),

    path('watchlist/', views.watchlist, name='watchlist'),
    path('add-watchlist/<int:movie_id>/<str:title>/',
         views.add_to_watchlist,
         name='add_watchlist'),
    path('remove-watchlist/<int:movie_id>/',
         views.remove_from_watchlist,
         name='remove_watchlist'),

    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('like/<int:movie_id>/', views.like_movie, name='like_movie'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
]