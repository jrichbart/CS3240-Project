from django.urls import path

from . import views

app_name = 'find'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:user>/', views.view_send_request, name='view_send_request'),
    path('<str:user>/view_send', views.send_buddy_request, name='view_buddy_request'),
]