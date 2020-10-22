from django.urls import path, include

from . import views

app_name = 'login'
urlpatterns = [
    path('', views.login, name='login'),
    path('account', views.account, name='account'),
    path('home', views.home, name='home')
]