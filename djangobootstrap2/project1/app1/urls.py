from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('', include("django.contrib.auth.urls")),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]