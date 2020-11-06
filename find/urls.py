from django.urls import path

from . import views

app_name = 'find'

urlpatterns = [
    path('', views.index, name='index'),
    
]