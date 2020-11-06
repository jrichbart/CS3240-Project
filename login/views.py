from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from userAccount.models import userAccount


def login(request):
    template = loader.get_template('login/login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def home(request):
    template = loader.get_template('login/home.html')
    if (userAccount.objects.filter(user=request.user).count() > 0):
        has_profile = True
    else:
        has_profile = False

    context = {
        'hasProfile': has_profile
    }
    return HttpResponse(template.render(context, request))

