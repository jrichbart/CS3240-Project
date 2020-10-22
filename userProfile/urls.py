from django.urls import path, include

from . import views

app_name = 'userProfile'
urlpatterns = [
    path('availability/', views.availability, name='availability')
]