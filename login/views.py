from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def login(request):
    template = loader.get_template('accounts/login.html')
    context = {}
    return HttpResponse(template.render(context, request))


def account(request):
    template = loader.get_template('accounts/accounts.html')
    context = {}
    return HttpResponse(template.render(context, request))

def home(request):
    template = loader.get_template('accounts/home.html')
    context = {}
    return HttpResponse(template.render(context, request))
