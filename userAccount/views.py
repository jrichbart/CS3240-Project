from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import userAccount

# Create your views here.

def index(request):
    return HttpResponse("Hello world")

def has_account(request):
    if(request.user.is_authenticated):
        if(userAccount.objects.filter(user=request.user).count()>0):
            return HttpResponseRedirect(reverse('userAccount:view_account'))
        else:
            user = request.user
            name = ""
            new_account = userAccount(user=user, name=name)
            new_account.save()
            return HttpResponseRedirect(reverse('userAccount:view_account'))
    else:
        return HttpResponseRedirect(reverse('login:login')) #figure out how to either add error message or redirect to google login

def view_account(request):
    currentUser = userAccount.objects.get(user=request.user)
    return HttpResponse("email: " + currentUser.user.email + " name: " + currentUser.name)