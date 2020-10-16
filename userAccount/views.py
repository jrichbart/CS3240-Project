from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    return HttpResponse("Hello world")

def view_account(request):
    if(request.user.is_authenticated):
        return HttpResponse(request.user.email)
    else:
        return HttpResponseRedirect(reverse('login:login')) #figure out how to either add error message or redirect to google login

def has_account(user):
    return False