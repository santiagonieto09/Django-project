"""
URL configuration for django_crud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from movies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('', views.user_home, name='user_home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('admin_movies/', views.admin_movies, name='admin_movies'),
    path('admin_create_movie/', views.create_movie, name='create_movie'),
    path('admin_movie/<int:movie_id>/', views.admin_movie_detail, name='admin_movie_detail'),
    path('admin_movie/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    path('user_available_movies/', views.user_available_movies, name='user_available_movies'),
    path('user_available_movie_detail/<int:movie_id>/', views.user_movie_detail, name='user_movie_detail'),
    path('user_available_movie/<int:movie_id>/add/', views.add_to_my_list, name='user_movie_add'),
    path('user_movies/', views.user_movies, name='user_movies'),
    path('user_movie_detail/<int:movie_id>/', views.user_movie_rating, name='user_movie_rating'),
    path('user_movie/<int:movie_id>/delete/', views.user_movie_delete, name='user_movie_delete'),
    path('user_movie/<int:movie_id>/rate/', views.user_movie_rate, name='user_movie_rate'),
    path('search/', views.search_results, name='search_results'),
    path('search_my_movies/', views.search_from_my_movies, name='search_from_my_movies'),
]
