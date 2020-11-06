from django.urls import path

from . import views

app_name = 'find'

urlpatterns = [
    path('', views.index, name='index'),
    path('<username>/', views.view_send_request, name='views_send_request'),
    path('<username>/', views.send_buddy_request, name='views_send_request'),
]