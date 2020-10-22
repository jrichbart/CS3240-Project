from django.urls import path, include

from . import views

app_name = 'userAccount'
urlpatterns = [
    path('availability/', views.availability, name='availability')
]