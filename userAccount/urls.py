from django.urls import path, include

from . import views

app_name = 'userAccount'
urlpatterns = [
    path('', views.view_account, name='view_account'),
    path('find/',views.has_account, name='has_account'),
    path('save/',views.save, name='save'),
    path('course/', views.course_form, name='course_form'),
    path('add/', views.add_course, name='add_course'),
    path('delete/', views.delete_course, name='delete_course'),
    path('availability/', views.availability, name='availability')
]