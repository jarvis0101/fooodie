from django.urls import path
from fooodie import views

app_name='fooodie'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('leaderboard/', views.leaderboard, name = 'leaderboard'),
    path('register/', views.register, name = 'register'),
    path('myprofile/', views.myprofile, name = 'myprofile'),
    path('user/<slug:user_profile_slug>/', views.user_profile, name='user_profile'),
    path('myprofile/add_food_photo/', views.add_food_photo, name='add_food_photo'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('loginregister/', views.user_signup_login, name='loginregister'),
    ]
"""path('add_photo/', views.add_photo, name='add_photo'),
path('user/<slug:user_name_slug>/', views.restricted, name='user'),
path('logout/', views.user_logout, name='logout'),"""
