from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('search/', views.search, name="search"),
    path('signup/', views.handleSignup, name="handleSignup"),
    path('login/', views.handleLogin, name="handleLogin"),
    path('logout/', views.handleLogout, name="handleLogout"),
    path('profile/', views.profile, name="profile"),
    path('pfp/', views.pfp, name="pfp"),
    path('password/',
         views.PasswordsChangeView.as_view(
             template_name="home/password_change.html"),
         name='password_change'),
]
