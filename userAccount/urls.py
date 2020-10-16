from django.urls import path

from . import views

app_name = 'userAccount'
urlpatterns = [
    path('', views.view_account, name='view_account')
]