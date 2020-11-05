from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from userAccount.models import userAccount, buddies, Course

def index(request):
    latest_account_list = userAccount.objects.all()
    all_courses = Course.objects.all()
    current_user_courses = []
    template = loader.get_template('buddies/index.html')
    currentUser = userAccount.objects.get(user=request.user)
    all_buddies_list = buddies.objects.all()
    for course in all_courses:
        if course.student == currentUser:
            current_user_courses.append(course)
    requester_confirmed_buddies_list = buddies.objects.filter(requester=currentUser, approved=True)
    requestee_confirmed_buddies_list = buddies.objects.filter(requestee=currentUser, approved=True)
    requester_buddies_list = buddies.objects.filter(requester=currentUser, approved=False)
    requestee_buddies_list = buddies.objects.filter(requestee=currentUser, approved=False)
    context = {
        'all_buddies_list': all_buddies_list,
        'requester_confirmed_buddies_list': requester_confirmed_buddies_list,
        'requestee_confirmed_buddies_list': requestee_confirmed_buddies_list,
        'requester_buddies_list': requester_buddies_list,
        'requestee_buddies_list': requestee_buddies_list,
        'all_courses': all_courses,
        'current_user_courses': current_user_courses,
        }
    return HttpResponse(template.render(context, request))