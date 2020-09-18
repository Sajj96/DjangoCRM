from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="login"),
    path('register/', views.register, name="register"),
    path('site/', views.site, name="site"),
    path('login/', views.logout_user, name="logout"),
    path('change_password/', views.change_password, name="change_password"),
]