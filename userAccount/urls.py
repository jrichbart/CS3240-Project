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
    path('find/availability/', views.has_availability, name='has_availability'),
    path('availability/', views.view_availability, name="view_availability"),
    path('availability/save', views.save_availability, name="save_availability"),
    path('buddies/', views.view_buddies, name='view_buddies'),
]