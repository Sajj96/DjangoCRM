from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name="login"),
    path('register/', views.register, name="register"),
    path('site/', views.site, name="site"),
    path('userlist/', views.userlist, name="userlist"),
    path('login/', views.logout_user, name="logout"),
    path('change_password/', views.change_password, name="change_password"),
    path('password_reset/', views.password_reset, name="password_reset"),
    path('reset_done/', views.reset_done, name="reset_done"),
    path('reset/<uidb64>/<token>/',views.reset_confirm, name='reset_confirm'),
    path('reset_complete/', views.reset_complete, name="reset_complete"),
]